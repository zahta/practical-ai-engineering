import json
import os
import urllib.error
import urllib.request

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AI Service")

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://host.docker.internal:11434",
).rstrip("/")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "120"))


class AnalyzeRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "provider": "ollama",
        "model": OLLAMA_MODEL,
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    prompt = (
        "Analyze the following text. Provide a concise, useful analysis "
        "in the same language as the input. Do not merely repeat the text.\n\n"
        f"Text:\n{request.text}"
    )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    http_request = urllib.request.Request(
        url=f"{OLLAMA_BASE_URL}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            http_request,
            timeout=OLLAMA_TIMEOUT,
        ) as response:
            ollama_data = json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise HTTPException(
            status_code=502,
            detail=f"Ollama returned HTTP {exc.code}: {detail[:500]}",
        ) from exc

    except (urllib.error.URLError, TimeoutError) as exc:
        raise HTTPException(
            status_code=504,
            detail=f"Could not get a timely response from Ollama: {exc}",
        ) from exc

    result = ollama_data.get("response")

    if not isinstance(result, str) or not result.strip():
        raise HTTPException(
            status_code=502,
            detail="Ollama returned an empty response.",
        )

    return {
        "result": result.strip(),
        "length": len(request.text),
        "provider": "ollama",
        "model": OLLAMA_MODEL,
    }
