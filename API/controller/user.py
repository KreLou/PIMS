import functools
from flask import Blueprint, g, redirect, request, session, url_for, jsonify, Response
from mysql.connector import cursor
from API.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

requiredFields = ['username', 'firstname', 'lastname', 'company', 'department']

#Strings
insert_User = ('insert into user'
               '(username, firstname, lastname, department, company, email, isuser, isagent, isadmin)'
               'values (%(username)s, %(firstname)s, %(lastname)s, %(department)s, %(company)s, %(email)s, %(isuser)s, %(isagent)s, %(isadmin)s)')

update_User = ('update user set '
               'username=%(username)s, '
               'firstname=%(firstname)s, '
               'lastname=%(lastname)s, '
               'department=%(department)s, '
               'company=%(company)s, '
               'email=%(email)s,'
               'isuser=%(isuser)s,'
               'isagent=%(isagent)s,'
               'isadmin=%(isadmin)s '
               'where id=%(id)s;')

myValues  = []
@bp.route('/', methods=('GET', 'POST'))
def values():
    db = get_db()
    cur = db.cursor()
    if request.method == 'GET':
        cur.execute('select id, username, firstname, lastname, department, company, email, enabled, isuser, isagent, isadmin from user where enabled = 1;')
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
                'enable': row[7],
                'isuser': row[8],
                'isagent': row[9],
                'isadmin': row[10]
            })
        return jsonify(json_data)
    else:
        body = request.get_json()

        for field in requiredFields:
            if not field in body or body[field] is None:
                return Response('No "{}"-Field found or field is empty (null/none)'.format(field), status=400)

        inputUser = {
            'firstname': body['firstname'] if 'firstname' in body else '',
            'lastname': body['lastname'] if 'lastname' in body else '',
            'username': body['username'] if 'username' in body else '',
            'department': body['department'] if 'department' in body else '',
            'company': body['company'] if 'company' in body else '',
            'email': body['email'] if 'email' in body else None,
            'isuser': body['isuser'] if 'isuser' in body else None,
            'isadmin': body['isadmin'] if 'isadmin' in body else None,
            'isagent': body['isagent'] if 'isagent' in body else None
        }
        print(inputUser)
        cur.execute(insert_User, inputUser)
        db.commit()
        userID = cur.lastrowid

        return jsonify(getUserById(userID)), 201

@bp.route('/<id>', methods=('GET', 'PUT', 'DELETE'))
def details(id):
    try:
        id = int(id)
    except ValueError:
        return Response('No valid ID', status=406)
    db = get_db()
    cur = db.cursor()
    if request.method == 'GET':
        return jsonify(getUserById(id))
    if request.method == 'PUT':
        body = request.get_json()

        for field in requiredFields:
            if not field in body or body[field] is None:
                return Response('No "{}"-Field found or field is empty (null/none)'.format(field), status=400)

        inputUser = {
            'id': id,
            'firstname': body['firstname'],
            'lastname': body['lastname'],
            'username': body['username'],
            'department': body['department'],
            'company': body['company'],
            'email': body['email'] if 'email' in body else None,
            'isuser': body['isuser'] if 'isuser' in body else None,
            'isagent': body['isagent'] if 'isagent' in body else None,
            'isadmin': body['isadmin'] if 'isadmin' in body else None
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
    cur.execute('select id, username, firstname, lastname, department, company, email, isuser, isadmin, isagent from user where id =' + str(id) + ';')
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
            'isuser': row[7],
            'isadmin': row[8],
            'isagent': row[9]
        }
        return user
    else:
        return None
