from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db

user_bp = Blueprint('user_bp', __name__ )

@user_bp.route("/users", methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])

    check_username = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()

    if check_username or check_email:
        return jsonify({'error': "Username or email already exists"})
    else:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': "User registered successfully"}), 201

    # Update the user account
@user_bp.route("/users/update", methods=['PATCH'])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if user:
        data = request.get_json()

        username = data.get('username', user.username)
        email = data.get('email', user.email)
        password = generate_password_hash(data.get('password', user.password))


        check_username = User.query.filter_by(username=username and id!=user.id).first()
        check_email = User.query.filter_by(email=email  and id!=user.id).first()

        if check_username or check_email:
            return jsonify({'error': "Username or email already exists"})
        else:
            user.username = username
            user.email = email
            user.password = password

            db.session.commit()

            return jsonify({'message': "User updated successful"})
    else:
        return jsonify({'error': "User not found"}), 404

# Delete a user
@user_bp.route("/users/delete_account", methods=['DELETE'])
@jwt_required()
def delete_user():
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if user:
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': "User deleted successfully"}), 200
    else:
        return jsonify({'error': "User not found"}), 404