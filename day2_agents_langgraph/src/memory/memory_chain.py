from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from config import MODEL_NAME
from memory.persistent_memory import load_persistent_history, append_turn

_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful task planning assistant. Use the conversation "
            "history - including anything the user mentioned in earlier "
            "sessions - to inform your answer. Reference specific earlier "
            "tasks when relevant.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
_llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
_base_chain = _prompt | _llm
_session_store: dict[str, InMemoryChatMessageHistory] = {}


def _get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _session_store:
        history = InMemoryChatMessageHistory()
        for turn in load_persistent_history():
            history.add_user_message(turn["input"])
            history.add_ai_message(turn["output"])
        _session_store[session_id] = history
    return _session_store[session_id]


_chain_with_memory = RunnableWithMessageHistory(
    _base_chain,
    _get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)


def chat(user_input: str, session_id: str = "default") -> str:
    result = _chain_with_memory.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}},
    )
    output = result.content
    append_turn(user_input, output)
    return output