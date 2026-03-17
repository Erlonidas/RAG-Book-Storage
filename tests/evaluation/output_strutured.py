from pydantic import BaseModel, Field

class EvalOutputStructured(BaseModel):
    reflection: str = Field(
        description="Your step-by-step thinking process: analyzing the chunks, formulating the question."
    )
    question: str = Field(
        description="A self-contained, challenging question generated strictly based on the provided reference chunks. Do not use phrases like 'in the text'."
    )
    ground_truth_answer: str = Field(
        description="The exact, direct answer to the generated question, extracted exclusively from the reference text without adding external knowledge."
    )

