def guardrail_check(guardrail_service_adapter):
    def validate(user_input: str) -> dict:

        return guardrail_service_adapter.run(user_input)
    return validate
