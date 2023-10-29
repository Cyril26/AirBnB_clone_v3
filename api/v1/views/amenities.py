#!/usr/bin/python3
""" Routes that handle all CRUD RestFul API actions for Amenities """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    all_amenities = storage.all(Amenity).values()
    amenities = []
    for amenity in all_amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a specific amenity with its id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a new Amenity object
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    amenity_data = request.get_json()

    if 'name' not in amenity_data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**amenity_data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an existing Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    amenity_data = request.get_json()

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in amenity_data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a specific Amenity Object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)