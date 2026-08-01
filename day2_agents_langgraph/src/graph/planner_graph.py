from langgraph.graph import StateGraph, END
from graph.state import PlannerState
from graph.nodes_summarize import summarize_node
from graph.nodes_classify import classify_node
from graph.nodes_prioritize import prioritize_node
from graph.nodes_plan import plan_node

_builder = StateGraph(PlannerState)

_builder.add_node("summarize", summarize_node)
_builder.add_node("classify", classify_node)
_builder.add_node("prioritize", prioritize_node)
_builder.add_node("plan", plan_node)

_builder.set_entry_point("summarize")
_builder.add_edge("summarize", "classify")
_builder.add_edge("classify", "prioritize")
_builder.add_edge("prioritize", "plan")
_builder.add_edge("plan", END)

planner_graph = _builder.compile()


def run_planner(task_input: str) -> PlannerState:
    """Run the full graph on a raw task input and return the final state."""
    result = planner_graph.invoke({"original_input": task_input})
    return result


def finalize_plan(original_input: str, approved_subtasks: str) -> PlannerState:
    state: PlannerState = {"original_input": original_input, "subtasks": approved_subtasks}
    state.update(classify_node(state))
    state.update(prioritize_node(state))
    state.update(plan_node(state))
    return state