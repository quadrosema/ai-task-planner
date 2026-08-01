from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from config import MODEL_NAME
from tools_agent.tools import ALL_TOOLS

_llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

tool_calling_agent = create_react_agent(
    model=_llm,
    tools=ALL_TOOLS,
    prompt=(
        "You are a helpful assistant with access to tools: a calculator, "
        "current date/time, weather lookup, Wikipedia search, and Google "
        "search. Use whichever tool(s) are relevant to answer the user's "
        "request. For date-math questions (e.g. days until a date), get "
        "today's date first, then use the calculator to compute the "
        "difference. Give a clear, direct final answer."
    ),
)


def ask(user_input: str) -> str:
    result = tool_calling_agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    return result["messages"][-1].content