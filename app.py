from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "habits.json"


def load_habits():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_habits(habits):
    with open(DATA_FILE, "w") as f:
        json.dump(habits, f, indent=2)


@app.route("/")
def index():
    habits = load_habits()
    return render_template("index.html", habits=habits)


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    if name:
        habits = load_habits()
        new_id = len(habits) + 1
        habits.append({"id": new_id, "name": name, "done": False})
        save_habits(habits)
    return redirect(url_for("index"))


@app.route("/done/<int:habit_id>", methods=["POST"])
def done(habit_id):
    habits = load_habits()
    for h in habits:
        if h["id"] == habit_id:
            h["done"] = True
    save_habits(habits)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
app.run(debug=True, port=5001)
