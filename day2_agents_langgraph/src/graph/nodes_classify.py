from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import MODEL_NAME
from graph.state import PlannerState

LABELS = ["Work", "Study", "Personal"]

_prompt = PromptTemplate(
    input_variables=["summary", "labels"],
    template=(
        "Classify the following task into exactly one of these categories: "
        "{labels}.\n\nRespond with ONLY the category name.\n\n"
        "Task:\n{summary}\n\nCategory:"
    ),
)
_llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
_chain = _prompt | _llm


def classify_node(state: PlannerState) -> PlannerState:
    result = _chain.invoke({"summary": state["summary"], "labels": ", ".join(LABELS)})
    label = result.content.strip()
    if label not in LABELS:
        label = "Personal"  
    return {"classification": label}