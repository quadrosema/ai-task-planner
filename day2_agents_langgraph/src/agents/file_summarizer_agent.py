from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from config import MODEL_NAME


@tool(description="Read and return the full text contents of a file at the given path.")
def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

summarizer_agent = create_react_agent(
    model=llm,
    tools=[read_file],
    prompt=(
        "You are a file summarization assistant. When given a file path, "
        "use the read_file tool to read its contents, then produce a "
        "concise 2-3 sentence summary of what the file contains. "
        "Respond with ONLY the summary, no preamble."
    ),
)


def summarize_file(path: str) -> str:
    result = summarizer_agent.invoke(
        {"messages": [{"role": "user", "content": f"Summarize the file at: {path}"}]}
    )
    return result["messages"][-1].content