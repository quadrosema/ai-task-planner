from datetime import date, datetime
import requests
from langchain_core.tools import tool
from config import OPENWEATHER_API_KEY, TAVILY_API_KEY


@tool(description="Evaluate a basic arithmetic expression, e.g. '15 * 3' or '(20 - 5) / 3'. Supports +, -, *, /, and parentheses only.")
def calculator(expression: str) -> str:
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed_chars):
        return "Error: expression contains disallowed characters."
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


@tool(description="Get the current date and time.")
def get_current_datetime() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S (%A)")


@tool(description="Get the current weather for a city name, e.g. 'Amman' or 'London'.")
def get_weather(city: str) -> str:
    if not OPENWEATHER_API_KEY:
        return "Error: OPENWEATHER_API_KEY is not configured."
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"{city}: {description}, {temp}\u00b0C"
    except Exception as e:
        return f"Error fetching weather: {e}"


@tool(description="Search Wikipedia for a topic and return a short summary.")
def wikipedia_search(query: str) -> str:
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            return f"No Wikipedia page found for '{query}'."
        response.raise_for_status()
        data = response.json()
        return data.get("extract", "No summary available.")
    except Exception as e:
        return f"Error searching Wikipedia: {e}"


@tool(description="Search Google (via Tavily) for current information on a topic or question.")
def google_search(query: str) -> str:
    if not TAVILY_API_KEY:
        return "Error: TAVILY_API_KEY is not configured."
    url = "https://api.tavily.com/search"
    payload = {"api_key": TAVILY_API_KEY, "query": query, "max_results": 3}
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if not results:
            return "No results found."
        summary_lines = [f"- {r['title']}: {r['content'][:200]}" for r in results]
        return "\n".join(summary_lines)
    except Exception as e:
        return f"Error searching: {e}"


ALL_TOOLS = [calculator, get_current_datetime, get_weather, wikipedia_search, google_search]