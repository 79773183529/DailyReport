import sqlite3
from dataclasses import dataclass
from enum import Enum


class SqliteEnum(Enum):
    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return self.value


class Post(SqliteEnum):
    PROJECT_MANAGER = "Руководитель проекта"
    PRECINCT_CHIEF = "Начальник участка"
    FOREMAN = "Прораб"
    BRIGADIER = "Бригадир"
    CONTRACTOR = "Представитель подрядчика"
    OTHER = "Другое"


@dataclass
class User:
    name: str
    lastname: str
    post: Post
    telegram_id: int
    is_active: bool

    def __str__(self):
        return f"Имя:  {self.name}\n" \
               f"Фамилия: {self.lastname}\n" \
               f"Должность: {self.post.value}"

    @property
    def args(self):
        return self.name, self.lastname, self.telegram_id

    def __eq__(self, other):
        if isinstance(other, User):
            return self.args == other.args
        else:
            raise NotImplemented

    def __hash__(self):
        return hash(self.args)

