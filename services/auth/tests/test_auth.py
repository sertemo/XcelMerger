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
from sqlalchemy.orm import sessionmaker, Session

from auth.src.main import (
    app,
    get_user,
    authenticate_user,
    create_access_token,
    get_password_hash,
    verify_password,
)
from auth.src.models import UserInDB
from common.databases.models import Base, User
from common.databases.engines import users_session

DATABASE_URL = "sqlite:///./test.db"


# Cliente de prueba
client = TestClient(app)
# Configuración de la base de datos de prueba
test_engine = create_engine(DATABASE_URL)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    # Cerrar todas las conexiones
    test_engine.dispose()
    # Eliminar el archivo de la base de datos
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture(scope="function")
def test_session(test_db):
    session = TestingSession()
    yield session
    session.close()


def override_users_session():
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()

# Sobreescribir el lifespan para evitar la inicialización de la base de datos real
async def override_lifespan(app):
    try:
        yield
    except Exception as e:
        raise

""" def test_login_for_access_token(test_session: Session):
    app.router.lifespan_context = override_lifespan
    app.dependency_overrides[users_session] = override_users_session
    # Añade un usuario de prueba a la base de datos
    hashed_password = get_password_hash("testpassword")
    user = User(
        username="testuser",
        hashed_password=hashed_password,
    )
    test_session.add(user)
    test_session.commit()

    # Datos de inicio de sesión
    login_data = {
        "username": "testuser",
        "password": "testpassword",
    }

    # Realiza una solicitud POST a /token con los datos de inicio de sesión
    response = client.post("/token", data=login_data)

    # Verifica la respuesta
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer" """

def test_authenticate_user_no_user(test_session: Session):
    user = authenticate_user("no_user", "wrongpassword", test_session)
    test_session.close()
    assert user is None


def test_authenticate_user_wrong_password(test_session: Session):
    # Añadimos en db un usuario
    user = User(
        username="pepe",
        hashed_password="lalalala",
    )
    test_session.add(user)
    user = authenticate_user("pepe", "wrongpassword", test_session)
    assert user is None


def test_authenticate_user_correct(test_session: Session):
    # Añadimos en db un usuario
    hashed_pwd = get_password_hash("lalalala")
    user = User(
        username="pepe",
        hashed_password=hashed_pwd,
    )
    test_session.add(user)
    test_session.commit()

    user = authenticate_user("pepe", "lalalala", test_session)
    print(f"{user=}")
    assert isinstance(user, UserInDB)


def test_verify_password():
    hashed_password = get_password_hash("mysecretpassword")
    assert verify_password("mysecretpassword", hashed_password)
    assert not verify_password("wrongpassword", hashed_password)


def test_create_access_token():
    token = create_access_token({"sub": "testuser"})
    assert token is not None
    assert isinstance(token, str)
