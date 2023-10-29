#!/usr/bin/python3
""" Routes that handle all CRUD RestFul API actions for Users """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects
    """
    all_users = storage.all(User).values()
    users = []
    for user in all_users:
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Retrieves a specific user with their id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new User object
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    user_data = request.get_json()

    if 'email' not in user_data:
        abort(400, description="Missing email")

    if 'password' not in user_data:
        abort(400, description="Missing password")

    new_user = User(**user_data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates an existing User object
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    user_data = request.get_json()

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']

    for key, value in user_data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a specific User Object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)