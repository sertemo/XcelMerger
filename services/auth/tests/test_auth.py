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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth.src.main import (
    app,
    get_user,
    authenticate_user,
    create_access_token,
    get_password_hash,
    verify_password,
)
from common.databases.models import Base, User
from common.databases.engines import users_session

DATABASE_URL = "sqlite:///./test.db"

# Configuración de la base de datos de prueba
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="module")
def client():
    def _get_test_db():
        return TestingSessionLocal()

    app.dependency_overrides[users_session] = _get_test_db
    with TestClient(app) as c:
        yield c


def test_verify_password():
    hashed_password = get_password_hash("mysecretpassword")
    assert verify_password("mysecretpassword", hashed_password)
    assert not verify_password("wrongpassword", hashed_password)


def test_create_access_token():
    token = create_access_token({"sub": "testuser"})
    assert token is not None
    assert isinstance(token, str)
