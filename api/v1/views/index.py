#!/usr/bin/python3
""" entry file index """
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_object_counts():
    """Retrieve the number of objects for each type"""
    object_types = [
        {"name": "amenities", "class": Amenity},
        {"name": "cities", "class": City},
        {"name": "places", "class": Place},
        {"name": "reviews", "class": Review},
        {"name": "states", "class": State},
        {"name": "users", "class": User}
    ]

    object_counts = {}

    for obj_type in object_types:
        count = storage.count(obj_type["class"])
        object_counts[obj_type["name"]] = count

    return jsonify(object_counts)