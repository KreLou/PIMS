import functools
from flask import Blueprint, g, redirect, request, session, url_for, jsonify, Response
from mysql.connector import cursor
from API.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

#Strings
insert_User = ('insert into user'
               '(username, firstname, lastname, department, company, email, ishuman)'
               'values (%(username)s, %(firstname)s, %(lastname)s, %(department)s, %(company)s, %(email)s, %(ishuman)s)')

update_User = ('update user set '
               'username=%(username)s, firstname=%(firstname)s, lastname=%(lastname)s, department=%(department)s, company=%(company)s, email=%(email)s, ishuman=%(ishuman)s '
               'where id=%(id)s;')

myValues  = []
@bp.route('/', methods=('GET', 'POST'))
def values():
    db = get_db()
    cur = db.cursor()
    if request.method == 'GET':
        cur.execute('select id, username, firstname, lastname, department, company, email, ishuman, enabled from user where enabled = 1;')
        rows = cur.fetchall()
        json_data = []
        for row in rows:
            json_data.append({
                'id': row[0],
                'username': row[1],
                'firstname': row[2],
                'lastname': row[3],
                'department': row[4],
                'company': row[5],
                'email': row[6],
                'ishuman': row[7],
                'enable': row[8]
            })
        return jsonify(json_data)
    else:
        body = request.get_json()

        inputUser = {
            'firstname': body['firstname'],
            'lastname': body['lastname'],
            'username': body['username'],
            'department': body['department'],
            'company': body['company'],
            'email': body['email'],
            'ishuman': body['ishuman']
        }
        print(inputUser)
        cur.execute(insert_User, inputUser)
        db.commit()
        inputUser['id'] = cur.lastrowid

        return jsonify(inputUser), 201

@bp.route('/<id>', methods=('GET', 'PUT', 'DELETE'))
def details(id):
    try:
        id = int(id)
    except ValueError:
        return Response('No valid ID', status=406)
    db = get_db()
    cur = db.cursor()
    if request.method == 'GET':
        cur.execute('select id, username, firstname, lastname, department, company, email, ishuman, enabled from user where id =' + str(id) + ';')
        row = cur.fetchone()
        if row is not None:
            user = {
                'id': row[0],
                'username': row[1],
                'firstname': row[2],
                'lastname': row[3],
                'department': row[4],
                'company': row[5],
                'email': row[6],
                'ishuman': row[7],
                'enable': row[8]
            }
            return jsonify(user)
        else:
            return jsonify(None), 404
    if request.method == 'PUT':
        body = request.get_json()

        inputUser = {
            'id': id,
            'firstname': body['firstname'],
            'lastname': body['lastname'],
            'username': body['username'],
            'department': body['department'],
            'company': body['company'],
            'email': body['email'],
            'ishuman': body['ishuman']
        }
        print(inputUser)
        cur.execute(update_User, inputUser)
        db.commit()
        return jsonify(getUserById(id))
    if request.method == 'DELETE':
        cur.execute('update user set enabled=0 where id={};'.format(id))
        db.commit()
        return ('', 204)


def getUserById(id):
    db = get_db()
    cur = db.cursor()
    cur.execute('select id, username, firstname, lastname, department, company, email, ishuman from user where id =' + str(id) + ';')
    row = cur.fetchone()
    if row is not None:
        user = {
            'id': row[0],
            'username': row[1],
            'firstname': row[2],
            'lastname': row[3],
            'department': row[4],
            'company': row[5],
            'email': row[6],
            'ishuman': row[7]
        }
        return user
    else:
        return None
