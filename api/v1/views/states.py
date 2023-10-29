#!/usr/bin/python3
""" Routes that handle all CRUD RestFul API actions for States """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects
    """
    all_states = storage.all(State).values()
    states = []
    for state in all_states:
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a specific State with id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State object
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    state_data = request.get_json()

    if 'name' not in state_data:
        abort(400, description="Missing name")

    new_state = State(**state_data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates an existing State object
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    state_data = request.get_json()

    if not state_data:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in state_data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State Object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)