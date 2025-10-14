from fastapi import APIRouter, HTTPException


router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Endpoint de health check para verificar se a API está funcionando.
    """
    try:
        return {"status": "ok", "message": "API está funcionando corretamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
