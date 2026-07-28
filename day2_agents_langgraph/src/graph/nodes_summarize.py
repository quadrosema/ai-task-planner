from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import MODEL_NAME
from graph.state import PlannerState

_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Summarize the following task description in 1-2 concise sentences, "
        "preserving any specific deadlines or important details.\n\n"
        "Task:\n{text}\n\nSummary:"
    ),
)
_llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
_chain = _prompt | _llm


def summarize_node(state: PlannerState) -> PlannerState:
    result = _chain.invoke({"text": state["original_input"]})
    return {"summary": result.content}