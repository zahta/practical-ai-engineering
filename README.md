# Practical AI Engineering

A small learning project that connects a FastAPI API, an Ollama-backed AI service, and n8n with Docker Compose.

## Services

- **API** (`fastapi-basic`): exposes example endpoints and forwards text-analysis requests.
- **AI service** (`ai-service`): sends prompts to Ollama and returns the generated result.
- **n8n**: provides a local workflow-automation interface.
- **Ollama**: runs on the host machine; the AI service connects to it at `http://host.docker.internal:11434`.

## Run locally

1. Install and start Docker Desktop and Ollama. Download the configured model:

   ```bash
   ollama pull qwen2.5:7b
   ```

2. From the repository root, start the services:

   ```bash
   docker compose up --build -d
   ```

3. Open the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs) or n8n at [http://localhost:5678](http://localhost:5678).

   ```bash
   curl -X POST http://localhost:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"text":"Explain why Docker Compose is useful."}'
   ```

Stop the services with `docker compose down`. n8n data is stored in the named `n8n_data` volume.

For setup details and learning notes, see the [Docker and FastAPI tutorial](docs/tutorial_docker_api.md), the [Docker Compose and AI service tutorial](docs/tutorial-docker-compose-fastapi-ai-service.md), and the [n8n workflow tutorial](docs/n8n.md).
