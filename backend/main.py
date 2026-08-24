from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent import run_user_query

app = FastAPI(
    title="GenAI Career Assistant API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {
        "message": "GenAI Career Assistant API is running"
    }


@app.post("/chat")
def chat(request: QueryRequest):

    try:
        result = run_user_query(request.query)

        return {
            "success": True,
            "category": result.get("category", ""),
            "response": result.get("response", "")
        }

    except Exception as e:

        error_message = str(e)

    if "429" in error_message:
        error_message = "Gemini API quota exceeded. Please try again later bro."

    return {
        "success": False,
        "error": error_message
    }