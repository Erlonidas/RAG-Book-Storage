from langgraph.graph import MessagesState
from typing import TypedDict, List, Dict, Optional, Annotated
from operator import add
from langchain_core.messages import BaseMessage

# <Considering only RAG step 2>
class Titles(TypedDict):
    title: str
    abstract: str


class Rag2Report(TypedDict):
    book_id: str
    sub_question: str
    rag_report: str
    retrieved_contexts: Optional[List[str]] #only for debug and evaluation


class InputRag(TypedDict):
    index_name: str # default
    query_vector: List[float]
    query_text: str
    book_id: str
    hybrid_text: Optional[str] | None
    

class MainState(MessagesState):
    possibles_pdfs_titles: List[Titles]
    decomposed_queries: List[Dict]
    retrieval_rag_input: InputRag
    retrieval_reports: Annotated[List[Rag2Report], add]
    guardrail_allowed: bool
# </Considering only RAG step 2>