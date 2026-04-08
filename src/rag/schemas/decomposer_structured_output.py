from pydantic import BaseModel, Field
from typing import List, TypedDict, Optional

class SubQueries(TypedDict):
    book_id: str = Field(description="exact book_id that you what make a search")
    sub_query: str = Field(description="sub query you what search related to the book_id")
    # keyword: str || X


class decomposer_structured_response(BaseModel):
    input_rag: Optional[List[SubQueries]] = Field(description="list of book_id followed by a sub query")