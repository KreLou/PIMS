from flask import Blueprint, request, jsonify, Response
from API.db import get_db
from API.controller import user
from API.controller.address import getAddressById, insertOrUpdateAddress

bp = Blueprint('package', __name__, url_prefix='/package')
requiredFields = ['tracking']

#Strings
insert_package = ('insert into package'
                  '(tracking,address_id, creator_id, receiver_id, confidential)'
                  'values (%(tracking)s, %(address_id)s, %(creator_id)s, %(receiver_id)s, %(confidential)s );')

update_package = ('update package set '
                  'address_id=%(address_id)s, '
                  'receiver_id=%(receiver_id)s, '
                  'isnotified=%(isnotified)s, '
                  'pickedup_at=%(pickedup_at)s, '
                  'confidential=%(confidential)s '
                  'where id=%(id)s;')


@bp.route('/', methods=('GET', 'POST'))
def getAllPackages():
    db = get_db()
    cur = db.cursor()
    if request.method == 'GET':
        cur.execute('select id, tracking, address_id, checkin_at, creator_id, receiver_id, isnotified, pickedup_at, confidential from package;')
        rows = cur.fetchall()
        json_data = []
        for row in rows:
            json_data.append({
                'id': row[0],
                'tracking': row[1],
                'address_id': row[2],
                'checkin': row[3],
                'creator': row[4],
                'receiver': row[5],
                'isnotified': row[6],
                'pickedup': row[7],
                'confidential': row[8]
            })
        return jsonify(json_data)
    if request.method == 'POST':
        user = 0 #TODO Define User by Token
        body = request.get_json()
        package = {'tracking': '', 'address_id': 0, 'creator_id': user, 'receiver_id': 0, 'confidential': 0 }
        if 'tracking' in body:
            package['tracking'] = body['tracking']
        if 'address_id' in body:
            package['address_id'] = body['address_id']
        if 'address' in body:
            package['address_id'] = insertOrUpdateAddress(body['address'])
        if 'receiver' in body:
            package['receiver_id'] = body['receiver']
        if 'confidential' in body:
            package['confidential'] = body['confidential']

        cur.execute(insert_package, package)
        db.commit()
        package['id'] = cur.lastrowid

        return jsonify(getPackageById(package['id'])), 201

@bp.route('/<id>', methods=('GET', 'PUT'))
def details(id):
    try:
        id = int(id)
    except ValueError:
        return Response('No valid Id', status=406)

    if request.method == 'GET':
        """Return the requested Package by ID"""
        return jsonify(getPackageById(id))

    if request.method == 'PUT':
        """Handling Package Update"""
        db = get_db()
        cur = db.cursor()
        body = request.get_json()
        insertPackage = {
            'id': id,
            'address_id': 0,
            'checkin': None,
            'creator_id': 0,
            'receiver_id': 0,
            'isnotified': False,
            'pickedup_at': None,
            'confidential': False,
            'tracking': ''
        }

        #Replaces all basic-fields
        #Trackingcode stays forever
        translator = ['checkin', 'creator_id', 'isnotified', 'pickedup_at', 'confidential', 'tracking']
        for key in translator:
            if key in body:
                insertPackage[key] = body[key]



        if 'address' in body and body['address'] is not None:
            insertPackage['address_id'] = insertOrUpdateAddress(body['address'])

        if 'receiver' in body and body['receiver'] is not None and body['receiver'] > 0:
            insertPackage['receiver_id'] = body['receiver']

        #Error Preventing
        if 'address_id' not in body:
            body['address_id'] = 0

        print(update_package)
        print(insertPackage)

        #Update in Database
        cur.execute(update_package, insertPackage)
        db.commit()
        return jsonify(getPackageById(body['id']))




def getPackageById(id):
    db = get_db()
    cur = db.cursor()
    cur.execute('select id, address_id, checkin_at, creator_id, receiver_id, isnotified, pickedup_at, confidential, tracking from package where id = {};'.format(id))
    row = cur.fetchone()
    if row is not None:
        package = {
            'id': row[0],
            'address': getAddressById(row[1]),
            'checkin': row[2],
            'creator': user.getUserById(row[3]),
            'receiver': user.getUserById(row[4]),
            'isNotified': row[5],
            'pickedup': row[6],
            'confidential': row[7],
            'tracking': row[8]
        }
        return package
    else:
        return None



