from datetime import date
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from config import MODEL_NAME
from graph.state import PlannerState


@tool(description="Get today's date, useful for judging urgency against any deadline mentioned in the task.")
def get_today_date() -> str:
    return date.today().isoformat()


_llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

_priority_agent = create_react_agent(
    model=_llm,
    tools=[get_today_date],
    prompt=(
        "You are a task prioritization assistant. Given a task summary and its "
        "category, decide a priority level: High, Medium, or Low. Use the "
        "get_today_date tool if the task mentions a deadline, to judge urgency. "
        "Consider both urgency (time pressure) and importance (impact of the "
        "category). Respond with ONLY one word: High, Medium, or Low."
    ),
)


def prioritize_node(state: PlannerState) -> PlannerState:
    message = (
        f"Subtasks: {state['subtasks']}\n"
        f"Category: {state['classification']}\n"
        "What is the priority?"
    )
    result = _priority_agent.invoke({"messages": [{"role": "user", "content": message}]})
    priority = result["messages"][-1].content.strip()
    if priority not in ("High", "Medium", "Low"):
        priority = "Medium"  
    return {"priority": priority}