#   Copyright 2024 Carlos García, Afonso Teixeira, Sergio Tejedor
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, session, url_for
import requests

from common.logging_config import logger
from common.settings import AUTH_SERVICE_URL


load_dotenv(dotenv_path="./common/.env")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    logger.info(f"Intento de login de usuario '{username}'")

    response = requests.post(
        f"{AUTH_SERVICE_URL}/token", data={"username": username, "password": password}
    )

    if response.status_code == 200:
        data = response.json()
        # Almacenamos el token y el nombre de usuario en sesión
        session["token"] = data["access_token"]
        session["username"] = username
        logger.info(f"Login de usuario '{username}' exitoso")
        return "", 200
    else:
        logger.info(f"Login de usuario '{username}' fallido")
        return "Usuario o contraseña incorrectos", 401


@app.route("/upload")
def upload():
    token = session.get("token")
    if not token:
        logger.info("El usuario no ha iniciado sesión. Redirigiendo al login")
        return redirect(url_for("index"))

    # Comprobamos si el token es válido
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{AUTH_SERVICE_URL}/users/me", headers=headers)
    username = session.get("username")

    if response.status_code == 200:
        logger.info(
            f"El usuario '{username}' ha iniciado sesión. Permitiendo el acceso"
        )
        return render_template("upload.html")
    else:
        logger.info(f"El token de '{username}' ha caducado. Redirigiendo al login")
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("token", None)
    return redirect(url_for("index"))
