# -*- coding:utf-8 -*-
# API для управления пользователями CRUD

from flask import Flask, request, jsonify, render_template
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import abort
from config import config
from model import User, db
from utils import create_app


app = create_app()

db.init_app(app)
with app.app_context():
    db.create_all()

# GET-запросы

@app.route('/')
@app.route('/home')
def home():
    try:
        return render_template('home.html')
    except TemplateNotFound:
        abort(404)


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    response = []
    for user in users:
        data = {
            'id': user.id,
            'email': user.email,
            'login': user.login,
            'password': user.password
        }
        response.append(data)
    if response == []:
        try:
            return render_template('empty_list.html')
        except TemplateNotFound:
            abort(404)
    return jsonify(response)


@app.route('/users/<int:id>', methods=['GET'])
def get_unique_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'email': user.email,
        'login': user.login
    })

# POST-запросы

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(email=data['email'], 
                    login=data['login'], 
                    password=data['password'])
    
    if new_user.email is None or new_user.login is None:
        return abort(404)
    
    # Check for unique value
    for user in User.query.all():
        if new_user.email in user.email:
            return abort(404)
        
        if new_user.login in user.login:
            return abort(404)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message':'new user created'})

# PUT-запросы

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({'message': 'User has not been found'}), 404
    
    data = request.json
    if 'login' in data:
        user.login = data['login']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']

    db.session.commit()

    return jsonify(user.to_json())


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if user is None:
        return jsonify({'message': 'user has not been found'}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify(User.query.get(id)), 200


if __name__ == '__main__':
    app.run(debug=True)
