from pydantic import BaseModel


class Titles(TypedDict):
    title: str
    abstract: str


class ChatRequest(BaseModel):
    possibles_pdfs_titles: List[Titles]
    messages: List
    session_id: str