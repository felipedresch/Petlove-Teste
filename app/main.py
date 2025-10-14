from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, questions_and_answers
from app.middleware import LoggingMiddleware

app = FastAPI(
    title="Petlove Assistente API",
    description="API de assistente inteligente usando FastAPI, Google Gemini e LangChain",
    version="0.1.0"
)

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"], prefix="/api")
app.include_router(questions_and_answers.router, tags=["Gemini"], prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=3000, reload=True)
