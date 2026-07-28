from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import MODEL_NAME

LABELS = ["Education", "Business", "Health", "Technology", "Personal/Other"]

classify_prompt = PromptTemplate(
    input_variables=["summary", "labels"],
    template=(
        "Classify the following text into exactly one of these categories: "
        "{labels}.\n\n"
        "Respond with ONLY the category name, nothing else.\n\n"
        "Text:\n{summary}\n\nCategory:"
    ),
)

llm = ChatOpenAI(model=MODEL_NAME, temperature=0.4)

classify_chain = LLMChain(llm=llm, prompt=classify_prompt)


def classify(summary: str) -> str:
    result = classify_chain.invoke({"summary": summary, "labels": ", ".join(LABELS)})
    label = result["text"].strip()
    return label if label in LABELS else "Personal/Other"