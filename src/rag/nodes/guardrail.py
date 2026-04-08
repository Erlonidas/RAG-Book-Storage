from langchain_core.messages import AIMessage


def guardrail(state, guardrail_port) -> dict:
    """
    Nó de segurança — primeira barreira do grafo.
    Extrai o texto da última HumanMessage e executa a validação via guardrail_port.
    Retorna 'guardrail_allowed' para o roteamento condicional.
    Se bloqueado, injeta uma AIMessage com o motivo no histórico.
    """
    last_human = next(
        (m for m in reversed(state["messages"]) if m.type == "human"),
        None,
    )
    user_input = last_human.content if last_human else ""

    result = guardrail_port(user_input)

    if not result["allowed"]:
        return {
            "guardrail_allowed": False,
            "messages": [AIMessage(content=f"Solicitação bloqueada: {result['reason']}")],
        }

    return {"guardrail_allowed": True}
