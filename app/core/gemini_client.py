from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings


def ask_gemini(pergunta: str) -> str:
    """
    Envia uma pergunta para o Google Gemini e retorna a resposta em texto.
    
    Args:
        pergunta: A pergunta a ser enviada ao Gemini
        
    Returns:
        str: A resposta do Gemini em texto simples
    """
    llm = ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=settings.GEMINI_TEMPERATURE
    )
    
    response = llm.invoke(pergunta)
    return response.content

