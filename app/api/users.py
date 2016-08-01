from flask import jsonify, request, current_app, url_for, redirect
from .. import mongo
from . import api
from ..models.User import User
from flask_login import login_user, logout_user, login_required


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/logout')
def logout():
    logout_user()
    return jsonify(success=True)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'message':'No data!'})
    if mongo.db.users.find_one({'email': data['email']}):
        return jsonify({'message':'The user is already exists!'})
    data['password'] = User.password(data['password'])
    mongo.db.users.save(data)
    return jsonify(success=True)




@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'message':'No data!'})
    user = mongo.db.users.find_one_or_404({'email': data['email']})
    #user = User.query.filter_by(email=data["email"]).first()
    if user and User.validate_login(user['password'], data['password']):
        user_obj = User(user['email'])
        login_user(user_obj)
        return jsonify({'token': user_obj.generate_auth_token(expiration=3600), 'expiration': 3600})
    return jsonify({'message':'No account!'})
