import os, random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")

# Render provides DATABASE_URL for Postgres. Fall back to local SQLite for dev.
db_url = os.environ.get("DATABASE_URL", "sqlite:///local.db")
# Heroku/Render sometimes give postgres://; SQLAlchemy expects postgresql://
db_url = db_url.replace("postgres://", "postgresql://")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.get("/")
def home():
    places = [p.name for p in Place.query.order_by(Place.name).all()]
    return render_template("index.html", places=places)

@app.post("/add")
def add_place():
    name = request.form.get("name", "").strip()
    if name:
        exists = Place.query.filter(Place.name.ilike(name)).first()
        if not exists:
            db.session.add(Place(name=name))
            db.session.commit()
    return redirect(url_for("home"))

@app.post("/delete")
def delete_place():
    name = request.form.get("name", "").strip()
    if name:
        Place.query.filter(Place.name.ilike(name)).delete(synchronize_session=False)
        db.session.commit()
    return redirect(url_for("home"))

@app.post("/spin")
def spin():
    places = [p.name for p in Place.query.all()]
    if not places:
        return jsonify({"error": "No places yet"}), 400
    choice = random.choice(places)
    return jsonify({"result": choice})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
