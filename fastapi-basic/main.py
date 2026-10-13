import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class UserRequest(BaseModel):
	name: str
	age: int


class AnalyzeRequest(BaseModel):
	text: str


@app.get("/hello")
def hello():
	return {"message": "Hello from FastAPI"}


@app.post("/users")
def  create_user(user: UserRequest):
	return{
		"message": f"Hello {user.name}!",
		"age": user.age
	}


@app.get("/users/{user_id}")
def get_user(user_id: int):
	return {
		"user_id": user_id,
	}


@app.get("/search")
def search_users(name:str, age:int | None = None):
	return {
		"name": name,
		"age": age,
	}



@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                "http://ai-service:8000/analyze",
                json={"text": request.text},
            )

        response.raise_for_status()

        return response.json()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="AI service timed out",
        )

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502,
            detail="AI service returned an error",
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="AI service is unavailable",
        )



@app.get("/config")
def config():
	return {
		"environment": os.getenv("APP_ENV", "development"),
		"llm_model": os.getenv("LLM_MODEL", "not-set"),
	}
