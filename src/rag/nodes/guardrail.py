from langchain_core.messages import AIMessage


def guardrail(state, guardrail_port) -> dict:
    last_human = next(
        (m for m in reversed(state["messages"]) if m.type == "human"),
        None,
    )
    user_input = last_human.content if last_human else ""

    result = guardrail_port(user_input)

    if not result["allowed"]:
        return {
            "guardrail_allowed": False,
            "messages": [AIMessage(content=f"Request blocked: {result['reason']} {result['blocked_at']}")]
        }

    return {"guardrail_allowed": True}
