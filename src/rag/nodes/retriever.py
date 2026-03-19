from src.rag.schemas.main_state import MainState
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
) 
from src.rag.prompts.retriever_prompt import (
    RETRIEVER_CONTEXT_SYS,
    ROUTER_QUESTION
) 

def retriever_rag(state: MainState, rag_port, chat_port):
    input_rag = state["retrieval_rag_input"]
    router_question_vector = input_rag["query_vector"]
    router_question_text = input_rag["query_text"]
    data_index = input_rag["index_name"]
    pdf_id = input_rag["book_id"]

    matched_chunks = rag_port(
        index_name=data_index,
        query_vector=router_question_vector,
        book_id=pdf_id,
        query_text=hybrid_text
    )
    ROUTER_PROMPT = ROUTER_QUESTION.format(
        router_question=router_question_text,
        all_chunks=matched_chunks)
    
    ai_response = chat_port.invoke([RETRIEVER_CONTEXT_SYS, ROUTER_PROMPT])
    main_state_update = {
        "retrieval_reports":[{
            "book_id": pdf_id,
            "sub_question": router_question_text,
            "rag_report": ai_response.content
        }]
    }

    return main_state_update