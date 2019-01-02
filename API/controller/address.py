from API.db import get_db


def getAddressById(id):
    db = get_db()
    cur = db.cursor()
    cur.execute('select id, company, firstname, lastname, street, housenr, zip, city, country, state from address where id = {};'.format(id))
    row = cur.fetchone()
    if row is not None:
        return {
            'id': row[0],
            'company': row[1],
            'firstname': row[2],
            'lastname': row[3],
            'street': row[4],
            'housenr': row[5],
            'zip': row[6],
            'city': row[7],
            'country': row[8],
            'state': row[9]
        }
    return None

def insertOrUpdateAddress(address):
    if address == None:
        return 0;
    db = get_db()
    cur = db.cursor()
    data = {
        'id': None,
        'company': '',
        'firstname': '',
        'lastname': '',
        'street': '',
        'housenr': '',
        'zip': '',
        'city': '',
        'country': '',
        'state': ''
    }

    if 'id' in address and address['id'] > 0:
        data['id'] = address['id']
    if 'company' in address:
        data['company'] = address['company']
    if 'firstname' in address and address['firstname'] != '':
        data['firstname'] = address['firstname']
    if 'lastname' in address and address['lastname'] != '':
        data['lastname'] = address['lastname']
    if 'street' in address and address['street'] != '':
        data['street'] = address['street']
    if 'housenr' in address and address['housenr'] != '':
        data['housenr'] = address['housenr']
    if 'zip' in address and address['zip'] != '':
        data['zip'] = address['zip']
    if 'city' in address and address['city'] != '':
        data['city'] = address['city']
    if 'country' in address and address['country'] != '':
        data['country'] = address['country']
    if 'state' in address and address['state'] != '':
        data['state'] = address['state']

    """Check if exists"""
    cur.execute('select id from address where company=%(company)s and '
                'firstname=%(firstname)s and '
                'lastname=%(lastname)s and '
                'street=%(street)s and '
                'housenr=%(housenr)s and '
                'zip=%(zip)s and '
                'city=%(city)s and '
                'country=%(country)s and '
                'state=%(state)s;', data)
    row = cur.fetchone()
    print('Housenummer:', str(data['housenr']), 'Length:', str(len(data['housenr'])))
    if row is not None:
        """Address allready exists"""
        return row[0]
    else:
        """Address not exists"""
        """New Address generated"""
        cur.execute('insert into address'
                    '(company, firstname, lastname, street, housenr, zip, city, country, state) values '
                    '(%(company)s, %(firstname)s, %(lastname)s, %(street)s, %(housenr)s, %(zip)s, %(city)s, %(country)s, %(state)s)', data)
        db.commit()
        return cur.lastrowid