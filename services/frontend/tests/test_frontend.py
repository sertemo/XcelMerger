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
import pytest
import requests
from flask import Flask, url_for
from flask.testing import FlaskClient
from dotenv import load_dotenv
from unittest.mock import patch

from frontend.src.app import (
    app,
)  # Asegúrate de importar correctamente tu aplicación Flask

load_dotenv(dotenv_path="./common/.env")


@pytest.fixture(scope="module")
def test_client() -> FlaskClient:
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["DEBUG"] = False
    return app.test_client()


@patch("requests.post")
def test_login_success(mock_post, test_client: FlaskClient):
    # Configurar el mock para devolver una respuesta exitosa
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"access_token": "test_token"}

    response = test_client.post(
        "/login", data={"username": "testuser", "password": "testpassword"}
    )

    assert response.status_code == 200
    with test_client.session_transaction() as sess:
        assert sess["token"] == "test_token"
        assert sess["username"] == "testuser"


@patch("requests.post")
def test_login_failure(mock_post, test_client: FlaskClient):
    # Configurar el mock para devolver una respuesta fallida
    mock_post.return_value.status_code = 401

    response = test_client.post(
        "/login", data={"username": "wronguser", "password": "wrongpassword"}
    )

    assert response.status_code == 401
    assert b"incorrectos" in response.data


@patch("requests.get")
def test_upload_access_granted(mock_get, test_client: FlaskClient):
    # Configurar el mock para devolver una respuesta exitosa
    mock_get.return_value.status_code = 200

    with test_client.session_transaction() as sess:
        sess["token"] = "test_token"
        sess["username"] = "testuser"

    response = test_client.get("/upload")
    assert response.status_code == 200
    assert (
        b"Carga archivos excels para agregar a la base de datos" in response.data
    )  # Verifica si el contenido renderizado es el esperado


@patch("requests.get")
def test_upload_access_denied(mock_get, test_client: FlaskClient):
    # Configurar el mock para devolver una respuesta fallida
    mock_get.return_value.status_code = 401

    with test_client.session_transaction() as sess:
        sess["token"] = "expired_token"
        sess["username"] = "testuser"

    with app.test_request_context():  # Nos aseguramos de que estamos en el contexto de los tests
        response = test_client.get("/upload")
        assert (
            response.status_code == 302
        )  # Redirigido al login, que está en la routa home (/)
        assert response.location == "/"
