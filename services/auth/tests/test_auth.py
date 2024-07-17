# Copyright 2024 Sergio Tejedor Moreno

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from datetime import timedelta
import os
from typing import Any

import pytest
from fastapi.testclient import TestClient
from common.settings import LOG_PATH

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
from auth.src.user_db import SQLManager, userdb_manager

client = TestClient(app)


# Set up a test database manager
@pytest.fixture(scope="module")
def test_db_manager():
    test_db = SQLManager(nombre_tabla="test_users", db_filename="test_users.db")
    SQLManager.create_table(
        db_filename="test_users.db",
        nombre_tabla="test_users",
        columnas=(
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "username TEXT",
            "full_name TEXT",
            "email TEXT",
            "hashed_password TEXT",
            "disabled BOOLEAN",
        ),
    )
    yield test_db
    os.remove("test_users.db")


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


def test_authenticate_user(test_db_manager, test_user):
    test_db_manager.insert_one(test_user)
    user = authenticate_user(test_db_manager, "testuser", "testpassword")
    assert user is not None
    assert user.username == "testuser"


def test_create_access_token():
    token = create_access_token({"sub": "testuser"})
    assert token is not None
    assert isinstance(token, str)


def test_login_for_access_token(test_db_manager, test_user):
    test_db_manager.insert_one(test_user)
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"


def test_read_users_me(test_db_manager, test_user):
    test_db_manager.insert_one(test_user)
    token = create_access_token({"sub": "testuser"})
    response = client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    user = response.json()
    assert user["username"] == "testuser"
    assert user["email"] == "testuser@example.com"
