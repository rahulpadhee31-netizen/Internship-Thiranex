from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
import sqlite3
import re

app = Flask(__name__)

# Secret key for sessions
app.secret_key = "change-this-to-a-random-secret-key"

bcrypt = Bcrypt(app)

DATABASE = "users.db"


# Connect to database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create users table
def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("home.html", username=session["username"])


# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        # Input validation
        if len(username) < 3:
            return "Username must contain at least 3 characters."

        if len(password) < 8:
            return "Password must contain at least 8 characters."

        if not re.search(r"[A-Za-z]", password):
            return "Password must contain a letter."

        if not re.search(r"[0-9]", password):
            return "Password must contain a number."

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        try:
            conn = get_db()

            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )

            conn.commit()
            conn.close()

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            return "Username already exists."

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        conn = get_db()

        # Parameterized query prevents SQL injection
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if user and bcrypt.check_password_hash(user["password"], password):

            session["username"] = user["username"]

            return redirect(url_for("home"))

        return "Invalid username or password."

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    create_table()

    app.run(debug=True)
