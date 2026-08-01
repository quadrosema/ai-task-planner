from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import MODEL_NAME

_prompt = PromptTemplate(
    input_variables=["original_task", "current_plan", "feedback"],
    template=(
        "Here is a task plan generated for this task:\n"
        "Original task: {original_task}\n\n"
        "Current plan:\n{current_plan}\n\n"
        "The user gave this feedback:\n{feedback}\n\n"
        "Update the plan according to the feedback. Keep the same format "
        "(a numbered list of subtasks). Respond with ONLY the updated "
        "numbered list, nothing else."
    ),
)
_llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
_chain = _prompt | _llm


def refine_plan(original_task: str, current_plan: str, feedback: str) -> str:
    result = _chain.invoke(
        {"original_task": original_task, "current_plan": current_plan, "feedback": feedback}
    )
    return result.content