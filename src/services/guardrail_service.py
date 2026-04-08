import re
from langchain_core.messages import HumanMessage, SystemMessage
from src.rag.prompts.guardrail_prompt import GUARDRAIL_SYSTEM_PROMPT, INJECTION_PATTERNS
from src.rag.schemas.guardrail_output_schema import GuardrailOutputSchema


class GuardrailService:
    def __init__(self, llm_client):
        self.llm = llm_client.with_structured_output(GuardrailOutputSchema)

    
    # layer 1: Regex
    def _check_injection(self, text: str):
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return f"Padrão suspeito detectado: '{pattern}'"
        return None


    #layer 2: LLM call
    def _llm_classify(self, text: str) -> dict:
        """Usa o LLM para classificar a intenção da mensagem."""
        messages = [
            SystemMessage(content=GUARDRAIL_SYSTEM_PROMPT),
            HumanMessage(content=text),
        ]
        try:
            result = self.llm.invoke(messages)
            return {
                "decision": result.decision,
                "reason": result.reason,
                "risk_level": result.risk_level,
            }
        except Exception as e:
            return {
                "decision": "BLOCKED",
                "reason": f"Erro ao classificar mensagem: {str(e)}",
                "risk_level": "high",
            }


    def run(self, user_input: str) -> dict:
        """
        Executa as camadas em ordem crescente de custo.

        Returns:
            dict com: allowed (bool), reason (str), risk_level (str), blocked_at (str | None)
        """
        # Camada 1 — Regex
        injection_reason = self._check_injection(user_input)
        if injection_reason:
            return {
                "allowed": False,
                "reason": injection_reason,
                "risk_level": "high",
                "blocked_at": "layer_1_regex",
            }

        # Camada 2 — LLM classifier
        llm_result = self._llm_classify(user_input)
        if llm_result["decision"] == "BLOCKED":
            return {
                "allowed": False,
                "reason": llm_result["reason"],
                "risk_level": llm_result["risk_level"],
                "blocked_at": "layer_2_llm",
            }

        return {
            "allowed": True,
            "reason": llm_result["reason"],
            "risk_level": llm_result["risk_level"],
            "blocked_at": None,
        }
