import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

_SPLITTER = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
_EMBEDDINGS = OpenAIEmbeddings(model="text-embedding-3-small")


def load_document(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(path)
    elif ext == ".docx":
        loader = Docx2txtLoader(path)
    elif ext in (".txt", ".md"):
        loader = TextLoader(path, encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {ext}. Supported: .pdf, .docx, .txt, .md")
    return loader.load()


def build_vector_store(path: str) -> InMemoryVectorStore:
    """Load a document, split it into chunks, embed the chunks, and return
    a vector store ready for retrieval."""
    documents = load_document(path)
    chunks = _SPLITTER.split_documents(documents)
    store = InMemoryVectorStore.from_documents(chunks, _EMBEDDINGS)
    return store