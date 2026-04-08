from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.rag.prompts.aggregator_prompt import (
    AGGREGATOR_SYS_MODE_ACADEMIC_PROMPT,
    AGGREGATOR_SYS_NON_ACADEMIC_PROMPT
)

def aggregator(state, aggregator_chat_port, academic_mode):
    messages = state["messages"]
    reports = "\n\n".join(
        f"- book_id: {rag_report['book_id']} | sub query: {rag_report['sub_question']} | answer: {rag_report['rag_report']}"
        for rag_report in state["retrieval_reports"]
    )
    system_prompt = AGGREGATOR_SYS_MODE_ACADEMIC_PROMPT.format(reports=reports) if academic_mode else AGGREGATOR_SYS_NON_ACADEMIC_PROMPT.format(reports=reports)
    ai_response = aggregator_chat_port.invoke([SystemMessage(system_prompt)] + messages)

    return {"messages": [AIMessage(content=ai_response.response)]}