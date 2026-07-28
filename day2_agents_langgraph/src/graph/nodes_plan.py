from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import MODEL_NAME
from graph.state import PlannerState

_prompt = PromptTemplate(
    input_variables=["summary", "classification", "priority"],
    template=(
        "Given this task:\n"
        "Summary: {summary}\n"
        "Category: {classification}\n"
        "Priority: {priority}\n\n"
        "Write a short (2-3 sentence) smart plan suggesting how and when "
        "the user should approach this task, given its priority."
    ),
)
_llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
_chain = _prompt | _llm


def plan_node(state: PlannerState) -> PlannerState:
    result = _chain.invoke(
        {
            "summary": state["summary"],
            "classification": state["classification"],
            "priority": state["priority"],
        }
    )
    return {"smart_plan": result.content}