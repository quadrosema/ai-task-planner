from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from config import MODEL_NAME

_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "Answer the question using ONLY the context below. If the context "
        "doesn't contain enough information to answer, say so explicitly - "
        "do not use any outside knowledge.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\nAnswer:"
    ),
)
_llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
_chain = _prompt | _llm


def build_qa_function(vector_store, k: int = 4):
    retriever = vector_store.as_retriever(search_kwargs={"k": k})

    def ask(question: str) -> str:
        retrieved_docs = retriever.invoke(question)
        context = "\n\n".join(doc.page_content for doc in retrieved_docs)
        result = _chain.invoke({"context": context, "question": question})
        return result.content

    return ask