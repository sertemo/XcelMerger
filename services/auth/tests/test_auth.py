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
from fastapi.testclient import TestClient
from datetime import timedelta
from typing import Any

from auth.src.main import (
    app,
    verify_password,
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_user,
    get_current_user,
    get_current_active_user,
    login_for_access_token,
    read_users_me,
)
from auth.src.models import Token, UserInDB, User
from auth.src.user_db import SQLManager, init_userdb

client = TestClient(app)

# Define una ruta de base de datos de prueba
TEST_DB_NAME = "test_users.db"


@pytest.fixture(scope="module")
def test_db_manager():
    init_userdb(db_filename=TEST_DB_NAME)  # Inicializa la base de datos de prueba
    yield SQLManager(nombre_tabla="users", db_filename=TEST_DB_NAME)
    os.remove(TEST_DB_NAME)


@pytest.fixture(scope="module")
def test_user():
    return {
        "username": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "hashed_password": get_password_hash("testpassword"),
        "disabled": False,
    }


def test_verify_password():
    hashed_password = get_password_hash("mysecretpassword")
    assert verify_password("mysecretpassword", hashed_password)
    assert not verify_password("wrongpassword", hashed_password)


def test_get_user(test_db_manager: SQLManager, test_user: dict[str, Any]):
    test_db_manager.insert_one(test_user)
    user = get_user(test_db_manager, "testuser")
    assert user is not None
    assert user.username == "testuser"


def test_authenticate_user(test_db_manager: SQLManager, test_user: dict[str, Any]):
    test_db_manager.insert_one(test_user)
    user = authenticate_user(test_db_manager, "testuser", "testpassword")
    assert user is not None
    assert user.username == "testuser"


def test_create_access_token():
    token = create_access_token({"sub": "testuser"})
    assert token is not None
    assert isinstance(token, str)
