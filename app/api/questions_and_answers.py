from fastapi import APIRouter, HTTPException, Depends
from app.schemas.question import QuestionRequest, AnswerResponse
from app.core.gemini_client import ask_gemini
from app.core.logger import logger
from app.core.security import verify_api_key

router = APIRouter()


@router.post(
    "/question-and-answer",
    response_model=AnswerResponse,
    summary="Enviar pergunta ao Gemini",
    description="Endpoint que recebe uma pergunta e retorna a resposta do Google Gemini",
    dependencies=[Depends(verify_api_key)]
)
async def question_and_answer(request: QuestionRequest) -> AnswerResponse:
    """
    Processa uma pergunta e retorna a resposta do Gemini.
    
    Args:
        request: Objeto contendo a pergunta
        
    Returns:
        AnswerResponse: Resposta do Gemini com metadados
        
    Raises:
        HTTPException: Em caso de erro ao processar a pergunta
    """
    try:
        response_text, metadata = ask_gemini(request.question)
        
        try:
            logger.log_question_answer(request.question, response_text)
        except Exception:
            pass
        
        return AnswerResponse(response=response_text, metadata=metadata)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar pergunta: {str(e)}"
        )

