import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin):  # Таблица пользователей
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Имя пользователя
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)  # Почта пользователя
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Хэшированный пароль
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)  # Дата создания аккаунта
    decks = orm.relationship("Decks", back_populates='user')

    def set_password(self, password):  # Функция для установки нового пароля
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):  # Функция для проверки пароля
        return check_password_hash(self.hashed_password, password)
