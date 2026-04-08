"""
Construção e compilação do grafo RAG multiagente.
Expõe `build_rag_graph()` para ser usado por endpoints.
"""
from langgraph.graph import START, END, StateGraph
from langgraph.constants import Send

from src.rag.schemas import MainState, ReactOutputStructured, decomposer_structured_response
from src.rag.nodes import retriever_rag, aggregator, router_decomposer, guardrail
from src.rag.ports import rag_search, EmbeddingPort, guardrail_check
from src.services import OpenSearchClient, create_llm, VectorProcessor, GuardrailService


def build_rag_graph(
    retriever_model: str = "gpt-4o-mini",
    reasoning_model: str = "gpt-4o",
    guardrail_model: str = "gpt-4o-mini",
    how_many_questions_decomposed: int = 3,
    k: int = 7,
    min_score: float = 0.4,
    academic_mode: bool = True,
):
    """
    Instancia as dependências e retorna o grafo RAG compilado.

    Args:
        retriever_model: Modelo usado no nó de retrieval.
        reasoning_model: Modelo usado no decomposer e aggregator.
        guardrail_model: Modelo usado no classificador LLM do guardrail.
        how_many_questions_decomposed: Número de sub-queries geradas pelo decomposer.
        k: Número de chunks retornados pelo OpenSearch.
        min_score: Score mínimo de similaridade para o OpenSearch.
        academic_mode: Se True, usa prompt acadêmico no aggregator.

    Returns:
        Grafo LangGraph compilado pronto para `.invoke()`.
    """
    # --- Adapters / clientes externos ---
    llm_retriever = create_llm(provider="openai", model=retriever_model)
    llm_reasoning = create_llm(provider="openai", model=reasoning_model)
    llm_guardrail = create_llm(provider="openai", model=guardrail_model)

    chat_decomposer = llm_reasoning.with_structured_output(decomposer_structured_response)
    chat_aggregator = llm_reasoning.with_structured_output(ReactOutputStructured)

    guardrail_service = GuardrailService(llm_client=llm_guardrail)

    opensearch_client = OpenSearchClient()
    rag_port = rag_search(opensearch_client)
    guardrail_port = guardrail_check(guardrail_service)
    embedding_converter = EmbeddingPort(VectorProcessor())

    # --- Definição dos nós com dependências injetadas via closure ---
    def guardrail_node(state: MainState):
        return guardrail(state=state, guardrail_port=guardrail_port)

    def router_node(state: MainState):
        return router_decomposer(
            state=state,
            embedding_converter_port=embedding_converter.convert_query,
            chat_output_structured_port=chat_decomposer,
            how_many_questions_decomposed=how_many_questions_decomposed,
        )

    def retriever_node(state: MainState):
        return retriever_rag(
            state=state,
            rag_port=rag_port,
            chat_port=llm_retriever,
            k=k,
            min_score=min_score,
        )

    def aggregator_node(state: MainState):
        return aggregator(
            state=state,
            aggregator_chat_port=chat_aggregator,
            academic_mode=academic_mode,
        )

    def async_rag_fan_out(state: MainState):
        return [
            Send("Agent_Rag", {"retrieval_rag_input": rag_input})
            for rag_input in state["decomposed_queries"]
        ]

    def route_after_guardrail(state: MainState):
        return "Router_Decomposer" if state["guardrail_allowed"] else END

    # --- Montagem do grafo ---
    builder = StateGraph(MainState)
    builder.add_node("Guardrail", guardrail_node)
    builder.add_node("Router_Decomposer", router_node)
    builder.add_node("Agent_Rag", retriever_node)
    builder.add_node("Aggregator", aggregator_node)

    builder.add_edge(START, "Guardrail")
    builder.add_conditional_edges("Guardrail", route_after_guardrail, ["Router_Decomposer", END])
    builder.add_conditional_edges("Router_Decomposer", async_rag_fan_out, ["Agent_Rag"])
    builder.add_edge("Agent_Rag", "Aggregator")
    builder.add_edge("Agent_Rag", END)

    return builder.compile()
