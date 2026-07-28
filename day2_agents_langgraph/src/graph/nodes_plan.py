from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import MODEL_NAME
from graph.state import PlannerState

_prompt = PromptTemplate(
    input_variables=["subtasks", "classification", "priority"],
    template=(
        "Given these subtasks:\n"
        "Subtasks: {subtasks}\n"
        "Category: {classification}\n"
        "Priority: {priority}\n\n"
        "Write a short smart plan suggesting the order to tackle these subtasks "
        "in, and roughly when, given the priority level."
    ),
)
_llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
_chain = _prompt | _llm


def plan_node(state: PlannerState) -> PlannerState:
    result = _chain.invoke(
        {
            "subtasks": state["subtasks"],
            "classification": state["classification"],
            "priority": state["priority"],
        }
    )
    return {"smart_plan": result.content}