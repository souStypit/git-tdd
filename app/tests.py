import os
import pytest 
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import User
from routes import app as flask_app, db as flask_db


@pytest.fixture(scope="module")
def app():
    return flask_app


@pytest.fixture(scope="module")
def db():
    return flask_db


@pytest.fixture(scope="module")
def client(app, db):
    client = app.test_client()

    ctx = app.app_context()
    ctx.push()
    db.create_all()

    yield client

    db.drop_all()
    ctx.pop()


# TDD

# GET /home

def test_home_status_code(client):
    response = client.get('/')
    assert response.status_code == 200


def test_home_data(client):
    homehtml = open('app/templates/home.html', 'r').read().encode()
    response = client.get('/')
    assert response.data == homehtml


# GET /users
def test_get_users_status_code(client):
    result = client.get('/users')
    assert result.status_code == 200


def test_get_users_empty_list(client):
    emptyhtml = open('app/templates/empty_list.html', 'r').read().encode()
    result = client.get('/users')
    assert result.data == emptyhtml


def test_get_users_with_data(client, db):
    user = User(email='test@example.com', login='test_login', password='12345')
    db.session.add(user)
    db.session.commit()

    result = client.get('/users')
    expected_response = [{
        'id': user.id,
        'email': 'test@example.com',
        'login': 'test_login',
        'password': '12345'
    }]

    assert json.loads(result.data) == expected_response


def test_get_unique_user(client):
    result = client.get('/users/1')
    expected_response = {
        'email': 'test@example.com',
        'id': 1,
        'login': 'test_login'
    }

    assert json.loads(result.data) == expected_response

# POST /users

def test_create_user_data(client):
    data = {
        'email': 'test@test.test',
        'login': 'testlogin',
        'password': '12345'
    }
    expected_response = {
        'email': 'test@test.test',
        'id': 2,
        'login': 'testlogin',
    }

    client.post('/users', json=data)
    result = json.loads(
        client.get('/users/2').data
    )
    assert result == expected_response


def test_create_user_non_unique_data(client):
    data = {
        'email': 'test@test.test',
        'login': 'testlogin',
        'password': '12345'
    }

    result = client.post('/users', json=data)
    assert result.status_code == 404


def test_create_user_missing_field(client):
    data = {
        'email': None,
        'login': 'testlogin',
        'password': '12345'
    }

    result = client.post('/users', json=data)
    assert result.status_code == 404


def test_change_user_status_code(client):
    id = 1
    result = client.put(f'/users/{id}', json={'id': id})
    assert result.status_code == 200
    

def test_change_user_data(client):
    id = 1
    data = {
        'id': id,
        'email': 'test@example.com',
        'login': 'test_new_login'
    }

    client.put(f'/users/{id}', json=data)
    result = client.get(f'/users/{id}')
    assert json.loads(result.data) == data
    

def test_change_user_no_data(client):
    id = 40
    result = client.put(f'/users/{id}', json={'id': id})
    assert result.status_code == 404


def test_delete_user(client, db):
    user = User(email='test@example.com', login='test_login', password='12345')
    db.session.add(user)
    db.session.commit()

    id = 1
    result = client.delete(f'/users/{id}', json={'id': id})
    assert result.status_code == 200
    assert json.loads(result.data) is None
    

def test_delete_user_not_exists(client, db):
    id = 1
    result = client.delete(f'/users/{id}', json={'id': id})
    assert result.status_code == 404
