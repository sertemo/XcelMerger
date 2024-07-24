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

from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated, Union
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from common.logging_config import logger
from common.settings import (
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    FRONTEND_SERVICE_URL,
)
from common.databases.engines import init_databases, Session_users
import common.databases.models as db_models
from .models import Token, TokenData, User, UserInDB


# Cargamos variables de entorno
load_dotenv(dotenv_path="./common/.env")

# Secret key to encode and decode JWT tokens
SECRET_KEY = os.getenv("SECRET_KEY")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializamos todas las bases de datos al iniciar la aplicación
    init_databases()
    logger.info("Bases de datos inicializadas correctamente")
    try:
        # Agregamos un user admin por defecto a la db de usuarios
        with Session_users.begin() as session:
            user = db_models.User(
                username="admin",
                hashed_password=os.getenv("ADMIN_PASS"),
                full_name="Usuario Admin para pruebas",
                email="tejedor.moreno.@gmail.com",
            )
            session.add(user)
            logger.info(f"User agregado correctamente: {user.username}")
        yield
    except Exception as e:
        logger.error(f"Error al inicializar las bases de datos: {e}")
        raise


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_SERVICE_URL],  # Allow only frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializamos el contexto de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Inicializamos el esquema de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña
    hasheada es correcta

    Parameters
    ----------
    plain_password : str
        _description_
    hashed_password : str
        _description_

    Returns
    -------
    bool
        True si son iguales
        False si son diferentes
    """
    verificacion: bool = pwd_context.verify(plain_password, hashed_password)
    return verificacion


def get_password_hash(password: str) -> str:
    """Hashea una contraseña utilizando
    el algoritmo bcrypt

    Parameters
    ----------
    password : str
        _description_

    Returns
    -------
    str
        _description_
    """
    hashed_password: str = pwd_context.hash(password)
    return hashed_password


def get_user(
    username: Union[str, None],
    session: Session,
) -> Optional[UserInDB]:
    """Devuelve un usuario dado su username o None
    si el usuario no se encuentra en la base de datos

    Parameters
    ----------
    username : Union[str, None]
        _description_
    session : Session
        La sesión abierta a la base de datos

    Returns
    -------
    Optional[UserInDB]
        _description_
    """
    if username is None:
        return None

    result: Optional[db_models.User] = (
        session.query(db_models.User)
        .filter(db_models.User.username == username)
        .first()
    )
    if result is None:
        return None
    return UserInDB(**result.to_dict())


def authenticate_user(
    username: str, password: str, session: Session
) -> Optional[UserInDB]:
    """Autentica un usuario:
    - Extrae el usuario username de la base de datos. Si no existe devuelve None
    - verifica la contraseña proporcionada con la contraseña hasheada del usuario

    Parameters
    ----------
    username : str
        _description_
    password : str
        _description_
    session_type : sessionmaker
        _description_

    Returns
    -------
    Optional[UserInDB]
        _description_
    """

    user = get_user(username, session)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(
    data: dict[str, Union[str, datetime]],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Crea un token JWT

    Parameters
    ----------
    data : dict
        _description_
    expires_delta : Optional[timedelta], optional
        _description_, by default None

    Returns
    -------
    str
        _description_
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    # Añadimos el tiempo de expiración al token
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se han podido verificar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict[str, str] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Union[str, None] = payload.get("sub")
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    # Abrimos una sesión con la base de datos de users
    with Session_users.begin() as session:
        user = get_user(username=token_data.username, session=session)
        if user is None:
            raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # Abrimos sesiones con la base de datos de users
    with Session_users.begin() as session:
        user = authenticate_user(
            form_data.username, form_data.password, session=session
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña o usuarios incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        usuario: str = user.username
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(usuario)}, expires_delta=access_token_expires
        )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


if __name__ == "__main__":
    pass
