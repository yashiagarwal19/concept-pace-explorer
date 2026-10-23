"""Concept Pace Explorer - Flask backend."""
import random
from flask import Flask, render_template, request, jsonify, redirect, url_for
import db, bandit
from lessons import LESSONS

app = Flask(__name__)
db.init()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    child = request.form.get("child", "").strip() or "Child-01"
    return redirect(url_for("lesson", child=child))

@app.route("/lesson/<child>")
def lesson(child):
    fmt = bandit.choose(db.stats(child))       # AI part: choose best format
    item = random.choice(LESSONS)
    return render_template("lesson.html", child=child, fmt=fmt, item=item)

@app.route("/api/log", methods=["POST"])
def log():
    d = request.get_json()
    r = bandit.reward(d["correct"], d["response_ms"], d["hints"])
    db.add_log(d["child"], d["fmt"], d["concept"], int(d["correct"]),
               d["response_ms"], d["hints"], r)
    return jsonify(ok=True, reward=r)

def summarize(rows):
    if not rows:
        return "No data yet."
    total = sum(r["n"] for r in rows)
    if total < 6:
        return "Not enough sessions yet (need about 6 answers)."
    best = max(rows, key=lambda r: r["avg_reward"])
    secs = sum(r["avg_ms"] * r["n"] for r in rows) / total / 1000
    pace = "answers quickly" if secs < 5 else "takes time to think" if secs > 12 else "works at a steady pace"
    return (f"Seems to learn best with {best['fmt']} (score {best['avg_reward']:.2f}, "
            f"{best['accuracy']:.0f}% correct). Usually {pace} (about {secs:.0f}s per answer). "
            "This is a learning preference, not a diagnosis.")

@app.route("/dashboard")
def dashboard():
    data = []
    for child in db.children():
        rows = [dict(r) for r in db.stats(child)]
        data.append({"child": child, "rows": rows, "summary": summarize(rows)})
    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
