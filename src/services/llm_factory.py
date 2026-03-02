"""
Factory para clientes LLM (OpenAI, Anthropic, etc).
Usado tanto na ingestão quanto no RAG.
"""
from typing import Optional, Literal
from langchain_openai import ChatOpenAI
from src.config import OPENAI_API_KEY, OPENAI_MODEL, ANTHROPIC_API_KEY, setup_logger

logger = setup_logger(__name__)

LLMProvider = Literal["openai", "anthropic"]


def create_llm(
    provider: LLMProvider = "openai",
    model: Optional[str] = None,
    temperature: float = 0.0,
    **kwargs
):
    """
    Cria um cliente LLM baseado no provider.
    
    Args:
        provider: Provider do LLM ("openai" ou "anthropic")
        model: Nome do modelo (usa default se None)
        temperature: Temperatura para geração
        **kwargs: Argumentos adicionais para o cliente
    
    Returns:
        Cliente LLM configurado
    """
    if provider == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não configurada")
        
        model = model or OPENAI_MODEL
        logger.info(f"Criando cliente OpenAI com modelo: {model}")
        
        return ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=model,
            temperature=temperature,
            **kwargs
        )
    
    elif provider == "anthropic":
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY não configurada")
        
        from langchain_anthropic import ChatAnthropic
        
        model = model or "claude-3-5-sonnet-20241022"
        logger.info(f"Criando cliente Anthropic com modelo: {model}")
        
        return ChatAnthropic(
            api_key=ANTHROPIC_API_KEY,
            model=model,
            temperature=temperature,
            **kwargs
        )
    
    else:
        raise ValueError(f"Provider '{provider}' não suportado")
