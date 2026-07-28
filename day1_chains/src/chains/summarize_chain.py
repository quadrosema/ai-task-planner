from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import MODEL_NAME

summarize_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Summarize the following text in 2-3 sentences. "
        "Be concise and keep only the key points.\n\n"
        "Text:\n{text}\n\nSummary:"
    ),
)

llm = ChatOpenAI(model=MODEL_NAME, temperature=0.2)

summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt)


def summarize(text: str) -> str:
    result = summarize_chain.invoke({"text": text})
    return result["text"]