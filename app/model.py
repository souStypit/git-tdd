# -*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


# Подключаемся к базе данных
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=True)
    login = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'login': self.login,
            'password': self.password
        }
