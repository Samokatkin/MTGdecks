import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Decks(SqlAlchemyBase):  # Таблица колод
    __tablename__ = 'decks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Название колоды
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Деклист
    commander1 = sqlalchemy.Column(sqlalchemy.String)  # Первый командир (если нужен)
    commander2 = sqlalchemy.Column(sqlalchemy.String)  # Второй командир (если нужен)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)  # Дата создания колоды
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)  # Приватная колода?

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    def __repr__(self):
        return f'{__class__.name} {self.name} {self.id} {self.email}'