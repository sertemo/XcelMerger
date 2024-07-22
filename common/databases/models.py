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

from typing import Any

from sqlalchemy import String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100))
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return (
            f"<[User]>(id={self.id}, "
            f"username={self.username}, "
            f"full_name={self.full_name})"
            f"email={self.email})"
        )

    def to_dict(self) -> dict[str, Any]:
        """Devuelve un diccionario con los datos del usuario

        Returns
        -------
        dict[str, str]
            _description_
        """
        return {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "hashed_password": self.hashed_password,
            "email": self.email,
            "disabled": self.disabled,
        }
