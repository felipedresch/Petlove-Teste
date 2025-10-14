from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """Schema para requisição de pergunta."""
    
    question: str = Field(
        ...,
        description="Pergunta a ser enviada ao Gemini",
        min_length=1,
        examples=["O que é a Petlove?"]
    )


class AnswerResponse(BaseModel):
    """Schema para resposta da pergunta."""
    
    response: str = Field(
        ...,
        description="Resposta retornada pelo Gemini",
        examples=["A Petlove é uma empresa de e-commerce que vende produtos para pets."]
    )
    metadata: dict = Field(
        default={},
        description="Metadados retornados pelo Gemini",
        examples=[{
            "model": "gemini-2.0-flash",
            "temperature": 0.7,
            "input_tokens": 100,
            "output_tokens": 50,
            "total_tokens": 150
        }]
    )

