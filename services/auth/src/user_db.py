#   Copyright 2024 Carlos García, Afonso Teixeira, Carlos, Sergio Tejedor
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
#   limitations under the License..

import os
import sqlite3
from sqlite3 import Cursor
from typing import Any, Optional

from dotenv import load_dotenv


load_dotenv()

DB_NAME = "users.db"


class SQLContext:
    """Clase para crear contextos de conexion
    a base de datos
    """

    def __init__(self, db_filename):
        self.db_filename = db_filename

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_filename)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class SQLManager:
    """ORM de lenguaje SQL con métodos para hacer operaciones
    con sqlite
    """

    def __init__(self, *, nombre_tabla: str, db_filename: str = DB_NAME) -> None:
        self.db_filename = db_filename
        self.tabla = nombre_tabla

    def get_table(self) -> list[tuple[str]]:
        """Devuelve una lista de tuplas conteniendo
        cada tupla los campos de cada columna
            para cada registro de la tabla dada"""
        with SQLContext(self.db_filename) as c:
            cursor: Cursor = c.execute(f"""SELECT * from {self.tabla}""")
            results: list[tuple[str]] = cursor.fetchall()
            return results

    def get_number_of_records(self) -> int:
        """Devuelve el número de registros

        Returns
        -------
        int
            _description_
        """
        return len(self.get_table())

    @property
    def columns_names(self) -> list[str]:
        """Devuelve una lista con el nombre de las columnas

        Returns
        -------
        list[str]
            _description_
        """
        with SQLContext(self.db_filename) as c:
            c.execute(f"PRAGMA table_info({self.tabla})")
            info = c.fetchall()
            column_names = [column[1] for column in info]
            return column_names

    def add_column(self, *, nombre_columna: str, tipo_dato: str) -> None:
        with SQLContext(self.db_filename) as c:
            c.execute(
                f"""ALTER TABLE
                {self.tabla} ADD COLUMN {nombre_columna} {tipo_dato}
                """
            )

    def add_column_nullable(self, *, nombre_columna: str, tipo_dato: str) -> None:
        with SQLContext(self.db_filename) as c:
            c.execute(
                f"""ALTER TABLE
                {self.tabla} ADD COLUMN {nombre_columna} {tipo_dato} NULL"""
            )

    def insert_one(self, columnas: dict[str, Any]) -> None:
        """inserta un registro en la tabla dada."""
        with SQLContext(self.db_filename) as c:
            query = f"""
            INSERT INTO {self.tabla} ({", ".join(columnas.keys())})
            VALUES ({", ".join('?' * len(columnas))})"""
            c.execute(query, tuple(columnas.values()))

    def find_one(
        self, *, campo_buscado: str, valor_buscado: str
    ) -> Optional[tuple[Any]]:
        """Devuelve todos los campos
        de la fila cuyo campo coincide
        con el valor buscado

        Parameters
        ----------
        campo_buscado : str
            _description_
        valor_buscado : str
            _description_

        Returns
        -------
        tuple[Any]
            _description_
        """
        with SQLContext(self.db_filename) as c:
            consulta = f"SELECT * FROM {self.tabla} WHERE {campo_buscado} = ?"
            cursor: Cursor = c.execute(consulta, (valor_buscado,))
            results: tuple[Any] = cursor.fetchone()
            return results

    def find_one_dict(
        self, *, campo_buscado: str, valor_buscado: str
    ) -> Optional[dict[str, Any]]:
        """Devuelve todos los campos
        de la fila cuyo campo coincide
        con el valor buscado. Devuelve en
        formato diccionario con los nombres
        de las columnas

        Parameters
        ----------
        campo_buscado : str
            _description_
        valor_buscado : str
            _description_

        Returns
        -------
        dict[str, Any]
            _description_
        """
        with SQLContext(self.db_filename) as c:
            consulta = f"SELECT * FROM {self.tabla} WHERE {campo_buscado} = ?"
            results = c.execute(consulta, (valor_buscado,)).fetchone()
            columnas = self.columns_names
            if results is None:
                return None
            return {k: v for k, v in zip(columnas, results)}

    def find_all(self, *, campo_buscado: str, valor_buscado: str) -> list[tuple[Any]]:
        """Devuelve todos los registros
        con todos los campos cuyo campo coincide
        con el valor buscado

        Parameters
        ----------
        campo_buscado : str
            _description_
        valor_buscado : str
            _description_

        Returns
        -------
        list[tuple[Any]]
            _description_
        """
        with SQLContext(self.db_filename) as c:
            consulta = f"SELECT * FROM {self.tabla} WHERE {campo_buscado} = ?"
            cursor: Cursor = c.execute(consulta, (valor_buscado,))
            results: list[tuple[Any]] = cursor.fetchall()
            return list(results)

    def find_one_field(
        self, *, campo_buscado: str, valor_buscado: str, campo_a_retornar: str
    ):
        """Devuelve todos el campo especificado
        de la fila cuyo campo coincide con el valor buscado

        Parameters
        ----------
        campo_buscado : str
            _description_
        valor_buscado : str
            _description_

        Returns
        -------
        _type_
            _description_
        """
        with SQLContext(self.db_filename) as c:
            consulta = f"""SELECT {campo_a_retornar}
            FROM {self.tabla}
            WHERE {campo_buscado} = ?"""
            results = c.execute(consulta, (valor_buscado,))
            if (output := results.fetchone()) is not None:
                return output[0]
            else:
                return output

    @classmethod
    def create_table(
        cls, *, db_filename: str, nombre_tabla: str, columnas: tuple[str, ...]
    ) -> None:
        with SQLContext(db_filename) as c:
            c.execute(
                f"CREATE TABLE IF NOT EXISTS {nombre_tabla} ({', '.join(columnas)})"
            )

    def delete_table(self) -> None:
        with SQLContext(self.db_filename) as c:
            c.execute(f"DELETE from {self.tabla}")
            c.execute(
                f"""
                    DELETE FROM sqlite_sequence WHERE name = '{self.tabla}'
                    """
            )  # Para reiniciar el autoincremental

    def delete_one(self, *, campo_buscado: str, valor_buscado: str) -> None:
        with SQLContext(self.db_filename) as c:
            consulta = f"DELETE FROM {self.tabla} WHERE {campo_buscado} = ?"
            c.execute(consulta, (valor_buscado,))

    def update_one(
        self,
        *,
        columna_a_actualizar: str,
        nuevo_valor: str,
        campo_buscado: str,
        valor_buscado: str,
    ) -> None:
        with SQLContext(self.db_filename) as c:
            consulta = f"""
            UPDATE {self.tabla}
            SET {columna_a_actualizar} = ? WHERE {campo_buscado} = ?
            """
            c.execute(consulta, (nuevo_valor, valor_buscado))

    def update_many(
        self,
        *,
        campo_buscado: str,
        valor_campo_buscado: str,
        columnas_a_actualizar: list[str],
        nuevos_valores: list[str | int],
    ) -> None:
        assert len(columnas_a_actualizar) == len(
            nuevos_valores
        ), "Las dos listas deben tener el mismo tamaño"
        # Comprobamos que las columnas a actualizar estén en la base de datos
        columnas = self.columns_names
        for col in columnas_a_actualizar:
            if col not in columnas:
                raise ValueError(f"La columna {col} " "no existe en la base de datos")
        with SQLContext(self.db_filename) as c:
            consulta = f"""
            UPDATE {self.tabla}
            SET {", ".join(col + ' = ?' for col in columnas_a_actualizar)}
            WHERE {campo_buscado} = ?;
            """
            c.execute(consulta, (*nuevos_valores, valor_campo_buscado))


# Inicializamos el administrador de la base de datos

userdb_manager = SQLManager(nombre_tabla="users", db_filename=DB_NAME)

# Creamos la tabla

SQLManager.create_table(
    db_filename=DB_NAME,
    nombre_tabla="users",
    columnas=(
        "id INTEGER PRIMARY KEY AUTOINCREMENT",
        "username TEXT",
        "full_name TEXT",
        "email TEXT",
        "hashed_password TEXT",
        "disabled BOOLEAN",
    ),
)

userdb_manager.insert_one(
    {
        "username": "admin",
        "full_name": "Usuario Admin para pruebas",
        "email": "tejedor.moreno@gmail.com",
        "hashed_password": os.getenv("ADMIN_PASS"),
        "disabled": False,
    }
)

userdb_manager.insert_one(
    {
        "username": "carlos",
        "full_name": "carlosalberto8717@gmail.com",
        "email": "carlos",
        "hashed_password": os.getenv("ADMIN_PASS"),
        "disabled": False,
    }
)
