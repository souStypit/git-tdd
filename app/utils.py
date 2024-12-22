from sys import argv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config


database_uri_key_index = 0
for i, k in enumerate(argv):
    if k == '--name':
        database_uri_key_index = i + 1
        break
database_uri_key = 'testing' if argv[database_uri_key_index] == 'TEST' else 'default'


def create_app(config_name=database_uri_key):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    return app
