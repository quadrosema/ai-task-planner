from flask import Flask, render_template, request
from graph.nodes_summarize import generate_subtasks
from graph.refine_plan import refine_plan
from graph.planner_graph import finalize_plan

app = Flask(__name__)
state = {"original_input": None, "current_plan": None, "final_result": None}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "task_input" in request.form:
            task_input = request.form["task_input"]
            state["original_input"] = task_input
            state["current_plan"] = generate_subtasks(task_input)
            state["final_result"] = None

        elif "approve" in request.form:
            state["final_result"] = finalize_plan(
                state["original_input"], state["current_plan"]
            )

        elif "feedback" in request.form:
            feedback = request.form["feedback"]
            state["current_plan"] = refine_plan(
                state["original_input"], state["current_plan"], feedback
            )

        elif "new_task" in request.form:
            state["original_input"] = None
            state["current_plan"] = None
            state["final_result"] = None

    return render_template(
        "index.html",
        original_input=state["original_input"],
        current_plan=state["current_plan"],
        final_result=state["final_result"],
    )


if __name__ == "__main__":
    app.run(debug=True)