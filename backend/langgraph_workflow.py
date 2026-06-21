from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from agents.planner import PlannerAgent
from agents.researcher import ResearchAgent
from agents.critic import CriticAgent
from agents.writer import WriterAgent
from agents.evaluator import EvaluatorAgent


class ResearchState(TypedDict):
    user_query: str
    plan: List[str]
    research_notes: List[Dict]
    critic_feedback: Optional[str]
    report: Optional[str]
    evaluation: Optional[str]
    approved: bool
    status: str
    retry_count: int


planner = PlannerAgent()
researcher = ResearchAgent()
critic = CriticAgent()
writer = WriterAgent()
evaluator = EvaluatorAgent()


def planning_node(state: ResearchState):
    print("LangGraph: Planning")
    state["plan"] = planner.create_plan(state["user_query"])
    state["status"] = "planned"
    return state


def research_node(state: ResearchState):
    print("LangGraph: Researching")
    state["research_notes"] = researcher.research(state["plan"])
    state["status"] = "researched"
    return state


def critic_node(state: ResearchState):
    print("LangGraph: Critic reviewing")
    state["critic_feedback"] = critic.review(state["research_notes"])
    state["status"] = "critic_reviewed"
    return state


def approval_node(state: ResearchState):
    print("LangGraph: Waiting for approval")
    state["status"] = "waiting_for_human_approval"
    return state


def writer_node(state: ResearchState):
    print("LangGraph: Writing report")
    state["report"] = writer.write_report(
        user_query=state["user_query"],
        plan=state["plan"],
        research_notes=state["research_notes"],
        critic_feedback=state["critic_feedback"]
    )
    state["status"] = "written"
    return state


def evaluator_node(state: ResearchState):
    print("LangGraph: Evaluating")
    state["evaluation"] = evaluator.evaluate(state["report"])
    state["status"] = "evaluated"
    return state


def retry_decision(state: ResearchState):
    evaluation = state.get("evaluation", "")
    retry_count = state.get("retry_count", 0)

    if retry_count >= 1:
        return "done"

    if "Score: 1" in evaluation or "Score: 2" in evaluation or "Score: 3" in evaluation or "Score: 4" in evaluation or "Score: 5" in evaluation or "Score: 6" in evaluation:
        state["retry_count"] = retry_count + 1
        return "retry"

    return "done"


def approval_decision(state: ResearchState):
    if state.get("approved") is True:
        return "approved"
    return "not_approved"


graph_builder = StateGraph(ResearchState)

graph_builder.add_node("planner", planning_node)
graph_builder.add_node("researcher", research_node)
graph_builder.add_node("critic", critic_node)
graph_builder.add_node("approval", approval_node)
graph_builder.add_node("writer", writer_node)
graph_builder.add_node("evaluator", evaluator_node)

graph_builder.set_entry_point("planner")

graph_builder.add_edge("planner", "researcher")
graph_builder.add_edge("researcher", "critic")
graph_builder.add_edge("critic", "approval")

graph_builder.add_conditional_edges(
    "approval",
    approval_decision,
    {
        "approved": "writer",
        "not_approved": END
    }
)

graph_builder.add_edge("writer", "evaluator")

graph_builder.add_conditional_edges(
    "evaluator",
    retry_decision,
    {
        "retry": "researcher",
        "done": END
    }
)

memory = MemorySaver()

graph = graph_builder.compile(checkpointer=memory)


def start_langgraph_workflow(user_query: str, thread_id: str):
    initial_state: ResearchState = {
        "user_query": user_query,
        "plan": [],
        "research_notes": [],
        "critic_feedback": None,
        "report": None,
        "evaluation": None,
        "approved": False,
        "status": "started",
        "retry_count": 0
    }

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = graph.invoke(initial_state, config)
    return result


def approve_and_continue(thread_id: str):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    current_state = graph.get_state(config).values
    current_state["approved"] = True
    current_state["status"] = "approved"

    result = graph.invoke(current_state, config)
    return result


def get_thread_state(thread_id: str):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    return graph.get_state(config).values
