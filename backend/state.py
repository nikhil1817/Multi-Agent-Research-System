from pydantic import BaseModel
from typing import List, Dict, Optional


class AgentState(BaseModel):
    user_query: str
    plan: List[str] = []
    research_notes: List[Dict] = []
    critic_feedback: Optional[str] = None
    report: Optional[str] = None
    evaluation: Optional[str] = None
