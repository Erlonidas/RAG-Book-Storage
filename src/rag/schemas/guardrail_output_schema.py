from pydantic import BaseModel, Field
from typing import Literal


class GuardrailOutputSchema(BaseModel):
    decision: Literal["ALLOWED", "BLOCKED"] = Field(
        description="Decision whether to allow or block the user message"
    )
    reason: str = Field(
        description="Short reason in english explaining the decision"
    )
    risk_level: Literal["low", "medium", "high"] = Field(
        description="Risk level assessment of the message"
    )
