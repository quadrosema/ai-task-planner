from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import MODEL_NAME
from graph.state import PlannerState

_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Break the following task down into 2-5 concrete, actionable subtasks. "
        "Preserve any specific deadlines or important details mentioned. "
        "Respond as a numbered list, one subtask per line, nothing else.\n\n"
        "Task:\n{text}\n\nSubtasks:"
    ),
)
_llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
_chain = _prompt | _llm


def generate_subtasks(text: str) -> str:
    result = _chain.invoke({"text": text})
    return result.content


def summarize_node(state: PlannerState) -> PlannerState:
    return {"subtasks": generate_subtasks(state["original_input"])}