from langgraph.graph import MessagesState
from typing import TypedDict, List, Dict, Optional, Annotated
from operator import add

# <Considering only RAG step 2>
class Titles(TypedDict):
    title: str
    abstract: str


class Rag2Report(TypedDict):
    book_id: str
    sub_question: str
    rag_report: str


class InputRag(TypedDict):
    index_name: str
    query_vector: List[float]
    query_text: str
    book_id: str
    hybrid_text: Optional[str] | None
    

class MainState(MessagesState):
    possibles_pdfs_titles: Optional[List[Titles]]
    retrieval_rag_input: InputRag
    retrieval_reports: Annotated[List[Rag2Report], add]
# </Considering only RAG step 2>