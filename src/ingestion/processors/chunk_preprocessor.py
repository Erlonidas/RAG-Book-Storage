from pathlib import Path
import os
import re
from src.services.llm_factory import create_llm
from src.ingestion.processors.chunk_builder import get_section_content
from src.ingestion.prompts.enhance_fig_tab_chunk import (
    SYSTEM_FIG_TREATMENT,
    SYSTEM_TABLE_TREATMENT,
    USER_FIG_REQUEST,
    USER_TABLE_REQUEST
)
from PIL import Image
import base64
from io import BytesIO
from langchain_core.messages import HumanMessage, SystemMessage
from src.config import setup_logger

logger = setup_logger(__name__)

class ContentAggregator:
    def __init__(self):
        self.chat_llm = create_llm(model="gpt-4o")
        self.project_root = Path(__file__).resolve().parents[3]


    def _find_url(self, content_with_url: str) -> str:
        pattern = r'!\[.*?\]\((.*?)\)'
        urls = re.findall(pattern, content_with_url)
        return urls[0] if urls else ""


    def _resolve_image_path(self, relative_path_from_json: str) -> str:

        # Monta o caminho: Raiz + data + raw + (figures/img.png)
        full_path = self.project_root / "data" / "raw" / relative_path_from_json
        return str(full_path)


    def centralize_section_context_for_element(self, complete_chunk_list: list) -> list:
        for index, doc in enumerate(complete_chunk_list):

            if doc["doc_type"] in ["figure", "table"]:
                type_content = doc["doc_type"]
                context = doc["content"]
                whole_section_content = get_section_content(
                    chunks = complete_chunk_list,
                    sec_1 = doc["sec_1"],
                    sec_2 = doc.get("sec_2")
                )
                match type_content:
                    case "figure":
                        raw_url = self._find_url(context)
                        url_fig = self._resolve_image_path(raw_url)
                        if not os.path.exists(url_fig):
                            print(f"Error: Figure imagem not found at: {url_fig}")
                            continue

                        chunk_fig = Image.open(url_fig)
                        buffered = BytesIO()
                        chunk_fig.save(buffered, format="PNG")
                        fig_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

                        system_message = SystemMessage(SYSTEM_FIG_TREATMENT)
                        complete_user_prompt = USER_FIG_REQUEST.format(
                            title=doc["sec_0"],
                            curr_content=doc["content"],
                            whole_section_content=whole_section_content
                        )
                        user_message = HumanMessage(
                            content=[
                                {'type': 'text', 'text': complete_user_prompt},
                                {'type': 'image_url', 'image_url': {
                                    'url': f"data:image/png;base64,{fig_b64}"
                                    }}
                            ]
                        )
                        ai_response = self.chat_llm.invoke([system_message, user_message])
                        augmented_context = ai_response.content
                        doc["image_metadata"] = url_fig
                        doc["content"] = doc["section_context"] + "\n\n<VISUAL_DESCRIPTION>" + augmented_context + "\n</VISUAL_DESCRIPTION>"
                        complete_chunk_list[index] = doc

                    case "table":
                        system_message = SystemMessage(SYSTEM_TABLE_TREATMENT)
                        complete_user_prompt = USER_TABLE_REQUEST.format(
                            title=doc["sec_0"],
                            curr_content=doc["content"],
                            whole_section_content=whole_section_content
                        )
                        user_message = HumanMessage(complete_user_prompt)
                        ai_response = self.chat_llm.invoke([system_message, user_message])
                        augmented_context = ai_response.content
                        doc["table_metadata"] = doc["content"]
                        doc["content"] = "<TABLE_DESCRIPTION>\n" + augmented_context + "\n</TABLE_DESCRIPTION>"
                        complete_chunk_list[index] = doc
        return complete_chunk_list
            