from fastapi import Header, HTTPException, status
from app.core.config import settings


async def verify_api_key(x_api_key: str = Header(..., description="Chave de API para autenticação")):
    """
    Verifica se a API Key fornecida no header é válida.
    """
    
    if not hasattr(settings, 'API_KEY') or not settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API Key não configurada no servidor"
        )
    
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida ou não autorizada"
        )
