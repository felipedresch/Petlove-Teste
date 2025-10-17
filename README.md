# Petlove AI Assistant

![CI/CD Pipeline](https://github.com/felipedresch/Petlove-Teste/actions/workflows/deploy.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)

API inteligente para responder perguntas sobre pets utilizando **Google Gemini**, **LangChain** e **FastAPI**.

**🌐 Demo em produção:** [https://fakepetloveapi.shop](https://fakepetloveapi.shop)

---

## Quick Start

### Pré-requisitos
- Python 3.11+
- [UV](https://github.com/astral-sh/uv) (recomendado) ou pip

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/felipedresch/Petlove-Teste.git
cd Petlove-Teste

# Instale as dependências
uv sync

# Configure as variáveis de ambiente
cp .env.example .env

# Execute a aplicação
uv run uvicorn app.main:app --port 3000 --reload
```

A API estará disponível em: `http://localhost:3000`

## Endpoints

### Health Check (público)
```bash
GET /api/health
```

**Resposta:**
```json
{
    "status": "ok",
    "message": "API está funcionando corretamente"
}
```

### Question & Answer (protegido)
```bash
POST /api/question-and-answer
Headers:
  x-api-key: sua-chave-aqui
  Content-Type: application/json

Body:
{
  "question": "Qual ração você recomenda para um filhote de labrador?"
}
```

**Exemplo de Resposta:**
```json
{
    "response": "Olá! Para um filhote de labrador, que é uma raça de porte grande com muita energia, {.....}",
    "metadata": {
        "model": "gemini-2.0-flash",
        "temperature": 0.7,
        "input_tokens": 236,
        "output_tokens": 285,
        "total_tokens": 521,
        "input_token_details": {
            "cache_read": 0
        }
    }
}

```

## Testes

```bash
# Rodar todos os testes
uv run pytest -v
```

**Cobertura de testes:**
- Health check endpoint
- Autenticação via API key
- Question & Answer com mocks do Gemini
- Tratamento de erros

---

## Arquitetura

```
app/
├── api/              # Endpoints HTTP
│   ├── health.py             # Health check
│   └── questions_and_answers.py  # Q&A endpoint
├── core/             # Lógica de negócio
│   ├── config.py             # Configurações
│   ├── gemini_client.py      # Cliente Gemini
│   ├── security.py           # Autenticação
│   └── logger.py             # Logging customizado
├── middleware/       # Middlewares
│   └── logging_middleware.py
├── schemas/          # Modelos Pydantic
│   └── question.py
└── main.py           # Entry point
```

### Stack Tecnológica

| Tecnologia | Uso |
|-----------|-----|
| **FastAPI** | Framework web moderno e assíncrono |
| **Uvicorn** | Servidor ASGI de alta performance |
| **LangChain** | Orquestração de LLMs |
| **Google Gemini** | Modelo de linguagem |
| **Pydantic** | Validação de dados |
| **Docker** | Containerização |
| **Traefik** | Reverse proxy + SSL automático |
| **GitHub Actions** | CI/CD automatizado |

---

## Logging

O sistema registra automaticamente:

- **`logs/api_requests.txt`**: Todas as requisições (método, rota, status, latência)
- **`logs/questions_answers.csv`**: Histórico de perguntas e respostas

Formato CSV:
```csv
timestamp,question,answer_preview
2025-10-16 10:30:00,"Qual ração para filhote?","Para filhotes de raças grandes..."
```

---

## Segurança

- Autenticação via API Key (header `x-api-key`)
- Rate limiting (via Traefik)
- Container não-root
- SSL/TLS automático (Let's Encrypt)
- Secrets gerenciados via GitHub Actions

---

## Deploy Automatizado

O projeto implementa **CI/CD completo** via GitHub Actions:

### Pipeline
1. **Push/PR** → Testes automatizados
2. **Tests pass** → Build da imagem Docker
3. **Merge na main** → Deploy automático na VM
4. **Health check** → Aplicação online

### Configuração

Adicione os seguintes **Secrets** no repositório GitHub:

| Secret | Descrição |
|--------|-----------|
| `VM_HOST` | IP ou domínio da VM |
| `VM_USER` | Usuário SSH |
| `VM_SSH_KEY` | Chave privada SSH |
| `GEMINI_API_KEY` | API Key do Google Gemini |

