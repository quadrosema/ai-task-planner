from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from config import MODEL_NAME


@tool(description="Count how many times a specific word appears in a file (case-insensitive).")
def count_word_in_file(path: str, word: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text.lower().count(word.lower())


llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

word_count_agent = create_react_agent(
    model=llm,
    tools=[count_word_in_file],
    prompt=(
        "You are a word-counting assistant. When given a file path and a "
        "target word, use the count_word_in_file tool to count occurrences, "
        "then respond with ONLY the number, no extra text."
    ),
)


def count_word(path: str, word: str) -> str:
    """Run the agent and return its final answer (the count, as reported by the agent)."""
    result = word_count_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Count how many times the word '{word}' appears in the file at: {path}",
                }
            ]
        }
    )
    return result["messages"][-1].content