import os
from functools import wraps
from datetime import datetime
import joblib
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db, init_db

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-before-deployment")
MODEL_PATH = os.path.join("models", "loan_model.pkl")

FEATURES = ["age", "annual_income", "employment_type", "education", "marital_status",
            "dependents", "loan_amount", "loan_term", "credit_score", "existing_debt", "loan_purpose"]

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Administrator access required.", "warning")
            return redirect(url_for("dashboard"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    return redirect(url_for("dashboard") if session.get("user_id") else url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not username or not email or len(password) < 8:
            flash("Enter all details. Password must contain at least 8 characters.", "danger")
            return render_template("register.html")
        db = get_db()
        try:
            db.execute("INSERT INTO users (username,email,password_hash,role) VALUES (?,?,?,?)",
                       (username, email, generate_password_hash(password), "user"))
            db.commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for("login"))
        except Exception:
            db.rollback()
            flash("That email may already be registered.", "danger")
        finally:
            db.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        db.close()
        if user and check_password_hash(user["password_hash"], password):
            session.update(user_id=user["id"], username=user["username"], role=user["role"])
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    rows = db.execute("SELECT * FROM prediction_history WHERE user_id=? ORDER BY created_at DESC LIMIT 5",
                      (session["user_id"],)).fetchall()
    count = db.execute("SELECT COUNT(*) AS n FROM prediction_history WHERE user_id=?",
                       (session["user_id"],)).fetchone()["n"]
    db.close()
    return render_template("dashboard.html", rows=rows, count=count)

@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    if request.method == "POST":
        try:
            values = {
                "age": int(request.form["age"]),
                "annual_income": float(request.form["annual_income"]),
                "employment_type": request.form["employment_type"],
                "education": request.form["education"],
                "marital_status": request.form["marital_status"],
                "dependents": int(request.form["dependents"]),
                "loan_amount": float(request.form["loan_amount"]),
                "loan_term": int(request.form["loan_term"]),
                "credit_score": int(request.form["credit_score"]),
                "existing_debt": float(request.form["existing_debt"]),
                "loan_purpose": request.form["loan_purpose"]
            }
            if not (18 <= values["age"] <= 100 and values["annual_income"] > 0 and
                    values["loan_amount"] > 0 and 300 <= values["credit_score"] <= 900 and
                    values["dependents"] >= 0 and values["loan_term"] > 0 and values["existing_debt"] >= 0):
                raise ValueError("Please check the numeric values.")
            model = joblib.load(MODEL_PATH)
            X = pd.DataFrame([values], columns=FEATURES)
            pred = int(model.predict(X)[0])
            confidence = round(float(max(model.predict_proba(X)[0])) * 100, 2)
            label = "High Risk" if pred == 1 else "Low Risk"
            db = get_db()
            db.execute("""INSERT INTO prediction_history
                (user_id,age,annual_income,employment_type,education,marital_status,dependents,
                 loan_amount,loan_term,credit_score,existing_debt,loan_purpose,prediction,confidence)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (session["user_id"], *[values[k] for k in FEATURES], label, confidence))
            db.commit()
            db.close()
            return render_template("result.html", label=label, confidence=confidence)
        except (ValueError, KeyError, FileNotFoundError) as e:
            flash(str(e) or "Invalid input. Please try again.", "danger")
        except Exception:
            flash("Prediction could not be completed. Train the model and check your database setup.", "danger")
    return render_template("predict.html")

@app.route("/history")
@login_required
def history():
    db = get_db()
    rows = db.execute("SELECT * FROM prediction_history WHERE user_id=? ORDER BY created_at DESC",
                      (session["user_id"],)).fetchall()
    db.close()
    return render_template("history.html", rows=rows)

@app.route("/admin")
@login_required
@admin_required
def admin():
    db = get_db()
    users = db.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
    total = db.execute("SELECT COUNT(*) AS n FROM prediction_history").fetchone()["n"]
    high = db.execute("SELECT COUNT(*) AS n FROM prediction_history WHERE prediction='High Risk'").fetchone()["n"]
    rows = db.execute("""SELECT p.*,u.username FROM prediction_history p
                         JOIN users u ON p.user_id=u.id ORDER BY p.created_at DESC LIMIT 100""").fetchall()
    db.close()
    return render_template("admin.html", users=users, total=total, high=high, rows=rows)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
