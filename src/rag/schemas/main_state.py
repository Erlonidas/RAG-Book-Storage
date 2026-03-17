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
    rag_report: Optional[str]
    

class MainState(MessagesState):
    possibles_pdfs_titles: Optional[List[Titles]]
    agent_rag_input: Rag2Report
    retrieval_reports: Annotated[List[Rag2Report], add]
# </Considering only RAG step 2>