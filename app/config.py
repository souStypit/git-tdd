# -*- coding:utf-8 -*-
import os


_SQLHEADER = 'sqlite:///'


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = _SQLHEADER + 'db.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = _SQLHEADER + 'test_db.db'


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}