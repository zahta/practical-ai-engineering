from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class AnalyzeRequest(BaseModel):
	text: str


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
	return {
		"result": f"AI analyzed: {request.text}",
		"length": len(request.text),
	}
