from ..services.llm_factory import create_llm
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

    def centralize_section_context_for_element(special_chunk: dict) -> dict:
        type_content = special_chunk["doc_type"]
        match type_content:
            case "figure":
                pass
            case "table":
                pass
        pass
        