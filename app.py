import random
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# ✅ Edit this list to “save” places in code
DEFAULT_PLACES = [
    "Nasi Kandar Ali",
    "Roti Canai Pak Din",
    "Mee Bandung Muar",
    "Sate Kajang",
]
PLACES = DEFAULT_PLACES.copy()

@app.get("/")
def home():
    return render_template("index.html", places=PLACES)

@app.post("/add")
def add_place():
    name = (request.form.get("name") or "").strip()
    if name and not any(p.lower() == name.lower() for p in PLACES):
        PLACES.append(name)
    return redirect(url_for("home"))

@app.post("/delete")
def delete_place():
    name = (request.form.get("name") or "").strip().lower()
    if name:
        for p in list(PLACES):
            if p.lower() == name:
                PLACES.remove(p)
    return redirect(url_for("home"))

@app.post("/spin")
def spin():
    if not PLACES:
        return jsonify({"error": "No places yet"}), 400
    return jsonify({"result": random.choice(PLACES)})

# Optional: restore the original hard-coded list at runtime
@app.post("/reset")
def reset():
    PLACES.clear()
    PLACES.extend(DEFAULT_PLACES)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
