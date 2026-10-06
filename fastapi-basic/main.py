import os
from fastapi import FastAPI
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
def analyze(request: AnalyzeRequest):
	return {
		"text": request.text,
		"length": len(request.text),
		"message": "Text received successfully!",
	}
