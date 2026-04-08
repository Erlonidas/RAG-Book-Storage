from pydantic import BaseModel, Field

class ReactOutputStructured(BaseModel):
    reasoning: str = Field(description="Reflection about contexts provided and its relation with the user's question")
    response: str = Field(description="Response for the users question")