import os

from flask import Flask, render_template, redirect, request, session, url_for
import requests

from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

AUTH_SERVICE_URL = "http://auth:8000"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    response = requests.post(
        f"{AUTH_SERVICE_URL}/token", data={"username": username, "password": password}
    )

    if response.status_code == 200:
        data = response.json()
        session["token"] = data["access_token"]
        return "", 200
    else:
        return "Usuario o contraseña incorrectos", 401


@app.route("/upload")
def upload():
    token = session.get("token")
    if not token:
        return redirect(url_for("index"))

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{AUTH_SERVICE_URL}/users/me", headers=headers)

    if response.status_code == 200:
        return render_template("upload.html")
    else:
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("token", None)
    return redirect(url_for("index"))
