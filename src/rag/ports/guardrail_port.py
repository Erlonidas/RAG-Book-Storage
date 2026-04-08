def guardrail_check(guardrail_service_adapter):
    """
    Port para o serviço de guardrail.
    Encapsula o GuardrailService (adapter) e expõe uma interface simples.
    
    Args:
        guardrail_service_adapter: instância de GuardrailService
        
    Returns:
        função que valida mensagens de usuário
    """
    def validate(user_input: str) -> dict:
        """
        Valida a mensagem do usuário através das camadas de segurança.
        
        Args:
            user_input: texto da mensagem do usuário
            
        Returns:
            dict com: allowed (bool), reason (str), risk_level (str), blocked_at (str | None)
        """
        return guardrail_service_adapter.run(user_input)
    
    return validate
