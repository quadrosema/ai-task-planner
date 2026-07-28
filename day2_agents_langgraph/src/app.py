from flask import Flask, render_template, request
from graph.planner_graph import run_planner

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        task_input = request.form["task_input"]
        result = run_planner(task_input)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)