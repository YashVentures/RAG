from dotenv import load_dotenv
from fastapi import FastAPI, Query
from .queues.worker import process_query, openai_client, vector_db
import redis
import os

load_dotenv()

app = FastAPI()

# In-memory chat history
chat_history = []

# Redis client for health check
redis_client = redis.Redis(host="localhost", port=6379)


@app.get("/")
def root():
    return {"status": "server is up and running"}


@app.post("/chat")
def chat(
    query: str = Query(..., description="The Chat query of user")
):
    result = process_query(query)

    # Store in history
    chat_history.append({
        "query": query,
        "response": result
    })

    return {"status": "done", "result": result}


@app.get("/history")
def get_history():
    return {
        "total": len(chat_history),
        "history": chat_history
    }


@app.delete("/history")
def clear_history():
    chat_history.clear()
    return {"status": "cleared", "message": "Chat history has been cleared"}


@app.get("/health")
def health_check():
    status = {}

    # Check Redis
    try:
        redis_client.ping()
        status["redis"] = "healthy"
    except Exception as e:
        status["redis"] = f"unhealthy - {str(e)}"

    # Check OpenAI
    try:
        openai_client.models.list()
        status["openai"] = "healthy"
    except Exception as e:
        status["openai"] = f"unhealthy - {str(e)}"

    # Check Qdrant
    try:
        vector_db.client.get_collections()
        status["qdrant"] = "healthy"
    except Exception as e:
        status["qdrant"] = f"unhealthy - {str(e)}"

    overall = "healthy" if all("healthy" == v for v in status.values()) else "degraded"

    return {
        "overall": overall,
        "services": status
    }