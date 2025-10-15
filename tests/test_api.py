import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_api_key():
    with patch("app.core.security.settings") as mock_settings:
        mock_settings.API_KEY = "test-api-key-123"
        yield mock_settings


class TestHealthEndpoint:
    """Testes para o endpoint de health check."""
    
    def test_health_check_returns_200(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
    
    def test_health_check_returns_correct_structure(self, client):
        response = client.get("/api/health")
        data = response.json()
        
        assert "status" in data
        assert "message" in data
        assert data["status"] == "ok"
        assert data["message"] == "API está funcionando corretamente"


class TestQuestionAndAnswerEndpoint:
    """Testes para o endpoint de perguntas e respostas."""
    
    def test_question_endpoint_requires_api_key(self, client):
        response = client.post(
            "/api/question-and-answer",
            json={"question": "Qual ração você recomenda?"}
        )
        assert response.status_code == 422  # sem o header x-api-key
    
    def test_question_endpoint_rejects_invalid_api_key(self, client, mock_api_key):
        response = client.post(
            "/api/question-and-answer",
            json={"question": "Qual ração você recomenda?"},
            headers={"x-api-key": "invalid-key"}
        )
        assert response.status_code == 401
        assert "inválida" in response.json()["detail"].lower()
    
    @patch("app.api.questions_and_answers.ask_gemini")
    def test_question_endpoint_returns_200_with_valid_key(self, mock_ask_gemini, client, mock_api_key):
        
        mock_ask_gemini.return_value = (
            "Para filhotes de labrador, recomendo ração específica para filhotes de raças grandes.",
            {
                "model": "gemini-2.0-flash",
                "temperature": 0.7,
                "input_tokens": 10,
                "output_tokens": 20,
                "total_tokens": 30
            }
        )
        
        response = client.post(
            "/api/question-and-answer",
            json={"question": "Qual ração você recomenda?"},
            headers={"x-api-key": "test-api-key-123"}
        )
        
        assert response.status_code == 200
    
    @patch("app.api.questions_and_answers.ask_gemini")
    def test_question_endpoint_returns_response_field(self, mock_ask_gemini, client, mock_api_key):
        mock_response = "Recomendo ração premium para filhotes."
        mock_metadata = {"model": "gemini-2.0-flash"}
        mock_ask_gemini.return_value = (mock_response, mock_metadata)
        
        response = client.post(
            "/api/question-and-answer",
            json={"question": "Qual ração você recomenda?"},
            headers={"x-api-key": "test-api-key-123"}
        )
        
        data = response.json()
        assert "response" in data
        assert data["response"] == mock_response
    
    @patch("app.api.questions_and_answers.ask_gemini")
    def test_question_endpoint_returns_metadata_field(self, mock_ask_gemini, client, mock_api_key):
        mock_metadata = {
            "model": "gemini-2.0-flash",
            "temperature": 0.7,
            "input_tokens": 15,
            "output_tokens": 25,
            "total_tokens": 40
        }
        mock_ask_gemini.return_value = ("Resposta do Gemini", mock_metadata)
        
        response = client.post(
            "/api/question-and-answer",
            json={"question": "Teste de metadados"},
            headers={"x-api-key": "test-api-key-123"}
        )
        
        data = response.json()
        assert "metadata" in data
        assert data["metadata"] == mock_metadata
    
    @patch("app.api.questions_and_answers.ask_gemini")
    def test_question_endpoint_handles_gemini_errors(self, mock_ask_gemini, client, mock_api_key):
        mock_ask_gemini.side_effect = Exception("Erro ao conectar com Gemini")
        
        response = client.post(
            "/api/question-and-answer",
            json={"question": "Teste de erro"},
            headers={"x-api-key": "test-api-key-123"}
        )
        
        assert response.status_code == 500
        assert "erro" in response.json()["detail"].lower()

