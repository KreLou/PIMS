import functools
from flask import Blueprint, g, redirect, request, session, url_for, jsonify, Response

from .db import get_db

bp = Blueprint('values', __name__, url_prefix='/values')

myValues = [
    {'id': 0, 'value': 'Test'},
    {'id': 1, 'value': 'World'}
]

@bp.route('/', methods=('GET', 'POST'))
def values():
    if request.method == 'GET':
        return jsonify(myValues)
    else:
        body = request.get_json()
        input = body['value']
        value = {}
        value['id'] = len(myValues)
        value['value'] = input
        myValues.append(value)
        return jsonify(value), 201

@bp.route('/<id>', methods=('GET', 'PUT'))
def details(id):
    try:
        id = int(id)
    except ValueError:
        return Response('No valid ID', status=406)
    if request.method == 'GET':
        result = [a for a in myValues if a['id'] == id]
        return jsonify(result)
    if request.method == 'PUT':
        body = request.get_json()
        value = body['value']
        for element in myValues:
            if element['id'] == id:
                element['value'] == value
                return jsonify(element), 200
        print(body)
        return jsonify({'Hello': 'World'})
