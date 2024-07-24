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


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.databases.models import Base
from common.settings import USER_DB_URL


users_engine = create_engine(USER_DB_URL, pool_size=10, max_overflow=20, echo=True)
Session_users = sessionmaker(autocommit=False, autoflush=False, bind=users_engine)


def init_databases():
    """Función que inicia todas las bases de datos
    creando las tablas correspondientes"""
    # import common.databases.models  # Importa los modelos aquí para que Base los reconozca

    # Creamos todas las bases de datos y sus tablas
    Base.metadata.create_all(bind=users_engine)
