import os
from rag.document_store import build_vector_store
from rag.qa_chain import build_qa_function

SAMPLE_DOC = os.path.join(os.path.dirname(__file__), "sample_docs", "lecture_notes.txt")

if __name__ == "__main__":
    print("Building vector store from sample lecture notes...")
    store = build_vector_store(SAMPLE_DOC)
    ask = build_qa_function(store)

    print("\nQ: Summarize Chapter 2.")
    print("A:", ask("Summarize Chapter 2."))

    print("\nQ: What is backpropagation?")
    print("A:", ask("What is backpropagation?"))

    print("\nQ: What does Chapter 5 say about robotics?")
    print("A:", ask("What does Chapter 5 say about robotics?"))