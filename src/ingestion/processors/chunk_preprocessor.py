from ..services.llm_factory import create_llm
from chunk_builder import get_section_content
from prompts import *
from PIL import Image
import base64
from io import BytesIO

from langchain_core.messages import HumanMessage, SystemMessage

class ContentAggregation:
    def __init__(self):
        self.chat_llm = create_llm(model="gpt-4o")

    def _find_url(self, content_with_url: str) -> str:
        pattern = r'!\[.*?\]\((.*?)\)'
        urls = re.findall(pattern, text)
        return urls

    def centralize_section_context_for_element(self, complete_chunk_list: dict) -> dict:
        all_special_chunks = []
        for doc in complete_chunk_list:
            if doc["doc_type"] != "text" and doc["doc_type"] == "figure" or doc["doc_type"] == "table":
                all_special_chunks.append(doc)

        for raw_chunk in all_special_chunks:  
            type_content = raw_chunk["doc_type"]
            context = raw_chunk["content"]
            whole_section_content = get_section_content(
                chunks = complete_chunk_list,
                sec_1 = raw_chunk["sec_1"],
                sec_2 = raw_chunk["sec_2"] if raw_chunk["sec_2"] else None,
            )
            match type_content:
                case "figure":
                    url_fig = self._find_url(context)
                    user_message = HumanMessage(
                        content=[
                            {'type': 'text', 'text': "Por favor, encontre o prato de comida na imagem, e identifique os alimentos que compoem esta refeição"},
                            {'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{img_b64}"}}
                        ]
                    )
                    ai_response = self.chat_llm.invoke([SystemMessage(SYSTEM_FIG_TREATMENT)]+[HumanMessage(USER_FIG_REQUEST)])
                    pass
                case "table":
                    pass
            pass
        