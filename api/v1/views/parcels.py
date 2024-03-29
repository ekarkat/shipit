#!/usr/bin/python3
"""
    Flask route that returns json response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


method = ['PUT', 'GET', 'POST', 'DELETE']

@app_views.route('/users/<user_id>/parcels', strict_slashes=False,
                 methods=method)
def user_parcels(user_id):
    """ just a discription"""
    user = storage.user_id(user_id)
    if not user:
        abort(404)

    if request.method == 'GET':
        parcels = user.user_parcels
        par_list = []
        for parcel in parcels:
            par_list.append(parcel.to_dict())
        return jsonify(par_list)

    # elif request.method == 'PUT':
    #     json_data = request.get_json(force=True, silent=True)
    #     if not json_data:
    #         abort(400, "Not a JSON")
    #     for key, value in json_data.items():
    #         if key == 'id' or key == 'created_at'\
    #                 or key == 'updated_at':
    #             continue
    #         else:
    #             setattr(user, key, value)
    #     user.save()
    #     return jsonify(user.to_dict()), 200

@app_views.route('/users/<user_id>/<parcel_id>', strict_slashes=False,
                 methods=method)
def user_parcel_id(user_id, parcel_id):
    user = storage.user_id(user_id)
    if not user:
        abort(404)
    parcel = storage.parcel_id(parcel_id)
    if not parcel:
        abort(404)

    if request.method == 'GET':
        return jsonify(parcel.to_dict())

    elif request.method == 'DELETE':
        # Delete a state
        storage.delete(parcel)
        storage.save()
        return jsonify({}), 200

@app_views.route('/parcels/<parcel_id>', strict_slashes=False,
                 methods=method)
def parcel_id(parcel_id):
    parcel = storage.parcel_id(parcel_id)
    if not parcel:
        abort(404)

    if request.method == 'GET':
        return jsonify(parcel.to_dict())

    elif request.method == 'DELETE':
        # Delete a state
        storage.delete(parcel)
        storage.save()
        return jsonify({}), 200
