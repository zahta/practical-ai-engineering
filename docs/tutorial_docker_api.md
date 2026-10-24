# Docker and FastAPI: Core Concepts

This tutorial introduces the API and container concepts used in this repository. It is a practical reference for the examples in `fastapi-basic` and the later Docker Compose tutorials.

## 1. APIs, HTTP, and REST

An **API** (Application Programming Interface) defines how software systems exchange requests and responses. Web APIs commonly use **HTTP** to carry those messages.

**REST** is a style for designing web APIs around resources and HTTP methods:

| Method | Typical purpose |
| --- | --- |
| `GET` | Read data |
| `POST` | Submit data or create a resource |
| `PUT` | Replace or update a resource |
| `DELETE` | Delete a resource |

FastAPI is a Python framework for building APIs; it is not itself an API. It generates an OpenAPI description of the application and provides interactive documentation at `/docs`.

## 2. Docker essentials

| Term | Meaning |
| --- | --- |
| Image | A packaged template used to create containers |
| Container | A running (or stopped) instance of an image |
| Dockerfile | Instructions for building an image |
| Docker Compose | A way to configure and run multiple related services |

For example, an Nginx container can publish its port to the host:

```bash
docker run -d --name my-nginx -p 8080:80 nginx
```

`-p 8080:80` maps host port `8080` to container port `80`. The service is then reachable from the host at `http://localhost:8080`.

Useful container commands:

```bash
docker ps                 # Running containers
docker ps -a              # Running and stopped containers
docker logs my-nginx      # Container output
docker exec -it my-nginx sh
docker stop my-nginx
docker start my-nginx
docker rm my-nginx
```

Use `docker exec` to run a command inside an already-running container. `docker logs` displays the container process output.

## 3. Build a small Python image

The `docker-python` directory contains a minimal Python application and Dockerfile:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

Build and run it from that directory:

```bash
docker build -t my-python-app .
docker run --name my-python-container my-python-app
```

The final `.` is the build context: the files Docker can use during the build. A short-lived application exits when its process finishes; an exited container is not necessarily an error.

`RUN` commands execute while an image is built. `CMD` sets the default command executed when a container starts.

## 4. FastAPI request and response basics

The `fastapi-basic` application demonstrates routes, request bodies, query parameters, and type validation.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserRequest(BaseModel):
    name: str
    age: int


@app.get("/hello")
def hello():
    return {"message": "Hello from FastAPI"}


@app.post("/users")
def create_user(user: UserRequest):
    return {"message": f"Hello {user.name}!", "age": user.age}
```

FastAPI converts returned Python dictionaries into JSON. Pydantic models define and validate JSON request bodies. An invalid value for a declared type normally produces a `422 Unprocessable Entity` response.

### Path parameters

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

`/users/42` supplies `42` as the path parameter. Because it is typed as an integer, `/users/not-a-number` fails validation.

### Query parameters

```python
@app.get("/search")
def search_users(name: str, age: int | None = None):
    return {"name": name, "age": age}
```

Call this endpoint with `GET /search?name=Sam&age=42`. The `name` query parameter is required, while `age` is optional.

### Request bodies

```python
class AnalyzeRequest(BaseModel):
    text: str
```

This model describes a JSON body such as `{"text":"Hello"}`. The current `/analyze` endpoint forwards its text to the separate AI service; it does not perform the model call inside the public API container.

## 5. Build and run the FastAPI container

The `fastapi-basic/Dockerfile` installs dependencies and starts FastAPI on all container interfaces at port `8000`. Build from the application directory:

```bash
cd fastapi-basic
docker build -t fastapi-basic .
docker run --name fastapi-basic-container -p 8000:8000 fastapi-basic
```

The port mapping publishes the container's port `8000` as host port `8000`. Visit:

- `http://localhost:8000/docs` for interactive API documentation
- `http://localhost:8000/hello` for a sample endpoint

Use `curl` to send a JSON request:

```bash
curl -i -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Sam","age":35}'
```

`-i` includes response headers, `-H` sets a header, and `-d` supplies the request body.

## 6. Status codes to recognize

| Status | Meaning in these examples |
| --- | --- |
| `200 OK` | Request completed successfully |
| `404 Not Found` | No route matches the requested URL |
| `422 Unprocessable Entity` | A path, query, or body value failed validation |
| `502 Bad Gateway` | A downstream service returned an unsuccessful response |
| `503 Service Unavailable` | The API could not connect to a downstream service |
| `504 Gateway Timeout` | A downstream operation exceeded its timeout |

## 7. Mental model

```text
Client or n8n
    │ HTTP request with JSON
    ▼
FastAPI ── validates inputs with Pydantic
    │
    ├── returns a JSON response
    └── or calls the AI service over HTTP
             │
             ▼
          Ollama
```

Docker packages each application into a container. Docker Compose connects the containers and provides service-name-based networking; see the [Compose and AI service tutorial](tutorial-docker-compose-fastapi-ai-service.md).

### Quick review

- **API:** a defined interface for software communication.
- **HTTP:** a common protocol for web requests and responses.
- **FastAPI:** a Python framework for building APIs.
- **Pydantic:** defines and validates structured data.
- **Docker image/container:** packaged application template / running instance.
- **Path, query, body:** the three common places API input is supplied.
- **OpenAPI and `/docs`:** API description and interactive documentation.
