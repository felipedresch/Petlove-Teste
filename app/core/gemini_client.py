from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings


def ask_gemini(pergunta: str) -> tuple[str, dict]:
    """
    Envia uma pergunta para o Google Gemini e retorna a resposta em texto com metadados.
    
    Args:
        pergunta: A pergunta a ser enviada ao Gemini
        
    Returns:
        tuple[str, dict]: Tupla contendo (resposta_texto, metadados)
    """
    llm = ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=settings.GEMINI_TEMPERATURE
    )
    
    response = llm.invoke(pergunta)
    
    metadata = {
        "model": settings.GEMINI_MODEL,
        "temperature": settings.GEMINI_TEMPERATURE,
    }
    
    if hasattr(response, 'usage_metadata'):
        metadata.update(response.usage_metadata)
    
    return response.content, metadata

