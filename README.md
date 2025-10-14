# Petlove Assistente API

API de assistente inteligente usando FastAPI, Google Gemini e LangChain.

## Setup

### Pré-requisitos
- Python 3.11+
- uv (recomendado) ou pip

### Instalação

1. Clone o repositório e navegue até a pasta:
```bash
cd petlove-teste
```

2. Instale as dependências:
```bash
uv sync
```

3. Execute a aplicação:
```bash
uv run python -m app.main
```

Ou usando uvicorn diretamente:
```bash
uv run uvicorn app.main:app --port 3000 --reload
```

### Testar a API

Acesse `http://127.0.0.1:3000/api/health` para verificar se a API está funcionando.

## 📁 Estrutura do Projeto

```
petlove-teste/
├── app/
│   ├── api/          # Rotas HTTP
│   ├── core/         # Lógica central (integrações, configs)
│   ├── schemas/      # Modelos Pydantic
│   └── main.py       # Aplicação FastAPI
├── tests/            # Testes
├── .gitignore
├── pyproject.toml    # Dependências do projeto
└── README.md
```

## Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validação de dados
- **LangChain** - Framework para aplicações com LLMs
- **Google Gemini** - Modelo de linguagem da Google
