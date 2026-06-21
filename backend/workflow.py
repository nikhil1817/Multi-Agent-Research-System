from backend.state import AgentState
from agents.planner import PlannerAgent
from agents.researcher import ResearchAgent
from agents.critic import CriticAgent
from agents.writer import WriterAgent
from agents.evaluator import EvaluatorAgent
from memory.store import save_memory


def run_agent_workflow(user_query: str):
    state = AgentState(user_query=user_query)

    planner = PlannerAgent()
    researcher = ResearchAgent()
    critic = CriticAgent()
    writer = WriterAgent()
    evaluator = EvaluatorAgent()

    print("Step 1: Planning...")
    state.plan = planner.create_plan(user_query)

    print("Step 2: Researching...")
    state.research_notes = researcher.research(state.plan)

    print("Step 3: Critic reviewing...")
    state.critic_feedback = critic.review(state.research_notes)

    print("Step 4: Writing report...")
    state.report = writer.write_report(
        user_query=state.user_query,
        plan=state.plan,
        research_notes=state.research_notes,
        critic_feedback=state.critic_feedback
    )

    print("Step 5: Evaluating report...")
    state.evaluation = evaluator.evaluate(state.report)

    save_memory(state.model_dump())

    return state
