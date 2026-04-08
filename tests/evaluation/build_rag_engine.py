from src.rag.schemas.main_state import MainState
from src.rag.prompts.retriever_prompt import (
    RETRIEVER_CONTEXT_SYS,
    ROUTER_QUESTION_TEMPLATE
)
from src.rag.nodes.retriever import retriever_rag
#ports
from src.rag.ports import (
    rag_search,
    llm_port,
    EmbeddingPort
)
#adapters
from src.services import (
    OpenSearchClient,
    create_llm, 
    VectorProcessor
)
from langgraph.graph import START, END, StateGraph


def retriver_node_builder(state: MainState):
    results_from_rag = retriever_rag(
        state=state,
        rag_port=rag_port,
        chat_port=chat,
        k=12,
        min_score=0.6
        )
    return results_from_rag


def graph_engine():
    chat = create_llm() #default = gpt-4o-mini
    opensearch_client = OpenSearchClient()
    rag_port = rag_search(opensearch_client)
    embedding_converter = EmbeddingPort(VectorProcessor()) 

    builder = StateGraph(MainState)
    builder.add_node("Agent_Rag", retriver_node_builder)
    builder.add_edge(START, "Agent_Rag")
    builder.add_edge("Agent_Rag", END)
    graph_execute = builder.compile()
    return graph_execute