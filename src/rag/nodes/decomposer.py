from langchain_core.messages import SystemMessage
from src.rag.prompts.decomposer_prompt import ROUTER_DECOMPOSER_SYS_PROMPT


def router_decomposer(
    state,
    embedding_converter_port,
    chat_output_structured_port,
    how_many_questions_decomposed,
):
    messages = state["messages"]
    possibles_pdfs = state.get("possibles_pdfs_titles", [])

    book_id_list = "\n".join(
        f"- book_id: {entry['title']} | abstract: {entry['abstract']}"
        for entry in possibles_pdfs
    )

    system_prompt = ROUTER_DECOMPOSER_SYS_PROMPT.format(
        how_many_questions_decomposed=how_many_questions_decomposed,
        book_id_list=book_id_list,
    )

    structured_response = chat_output_structured_port.invoke(
        [SystemMessage(system_prompt)] + messages
    )

    sends = []
    for sub_query in structured_response.input_rag:
        query_text = sub_query["sub_query"]
        query_vector = embedding_converter_port(query_text)
        sends.append(
                {
                    "index_name": "content-pdfs",
                    "query_vector": query_vector,
                    "query_text": query_text,
                    "book_id": sub_query["book_id"],
                    "hybrid_text": None,
                }
        )

    return {"decomposed_queries": sends}
