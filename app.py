from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

DATA_FILE = "habits.json"


# -------------------------
# DATA
# -------------------------

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


# -------------------------
# STREAK
# -------------------------

def get_streak(completions):
    if not completions:
        return 0

    completions = set(completions)
    streak = 0
    today = datetime.now()

    for i in range(365):
        day = today - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")

        if day_str in completions:
            streak += 1
        else:
            break

    return streak


# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def index():
    habits = load_habits()

    for h in habits:
        if "completions" not in h:
            h["completions"] = []
        h["streak"] = get_streak(h["completions"])

    return render_template("index.html", habits=habits)


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")

    if name:
        habits = load_habits()

        habits.append({
            "id": len(habits) + 1,
            "name": name,
            "completions": []
        })

        save_habits(habits)

    return redirect(url_for("index"))


@app.route("/done/<int:habit_id>", methods=["POST"])
def done(habit_id):
    habits = load_habits()
    today = datetime.now().strftime("%Y-%m-%d")

    for h in habits:
        if h["id"] == habit_id:
            if "completions" not in h:
                h["completions"] = []

            if today not in h["completions"]:
                h["completions"].append(today)

    save_habits(habits)
    return redirect(url_for("index"))


# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
