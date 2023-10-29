#!/usr/bin/python3
""" Routes that handle all CRUD RestFul API actions for a place's Reviews."""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects linked to a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a specific Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    review_data = request.get_json()

    if 'user_id' not in review_data:
        abort(400, description="Missing user_id")

    user = storage.get(User, review_data['user_id'])

    if not user:
        abort(404)

    if 'text' not in review_data:
        abort(400, description="Missing text")

    review_data['place_id'] = place_id
    new_review = Review(**review_data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates an existing Review object
    """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    review_data = request.get_json()
    for key, value in review_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a specific Review Object
    """

    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)