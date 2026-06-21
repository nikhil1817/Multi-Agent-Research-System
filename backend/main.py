from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4

from backend.langgraph_workflow import (
    start_langgraph_workflow,
    approve_and_continue,
    get_thread_state
)

app = FastAPI(title="LangGraph Research Agent System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    query: str


class ThreadRequest(BaseModel):
    thread_id: str


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "LangGraph Research Agent System is live"
    }


@app.post("/langgraph/start")
def start_research(request: ResearchRequest):
    thread_id = str(uuid4())

    result = start_langgraph_workflow(
        user_query=request.query,
        thread_id=thread_id
    )

    return {
        "thread_id": thread_id,
        "result": result
    }


@app.post("/langgraph/approve")
def approve(request: ThreadRequest):
    result = approve_and_continue(request.thread_id)

    return {
        "thread_id": request.thread_id,
        "result": result
    }


@app.get("/langgraph/state/{thread_id}")
def state(thread_id: str):
    result = get_thread_state(thread_id)

    return {
        "thread_id": thread_id,
        "state": result
    }
