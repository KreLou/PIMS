from API.db import get_db


def getAddressById(id):
    db = get_db()
    cur = db.cursor()
    cur.execute('select id, company, firstname, lastname, street, housenr, zip, city, country from address where id = {};'.format(id))
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
            'country': row[8]
        }
    return None

def insertOrUpdateAddress(address):
    if address == None:
        return 0;
    db = get_db()
    cur = db.cursor()
    id = None
    company = None
    firstname = None
    lastname = None
    street = None
    housenr = None
    zip = None
    city = None
    country = None
    if 'id' in address and address['id'] > 0:
        id = address['id']
    if 'company' in address:
        company = address['company']
    if 'firstname' in address and address['firstname'] != '':
        firstname = address['firstname']
    if 'lastname' in address and address['lastname'] != '':
        lastname = address['lastname']
    if 'street' in address and address['street'] != '':
        street = address['street']
    if 'housenr' in address and address['housenr'] != '':
        housenr = address['street']
    if 'zip' in address and address['zip'] != '':
        zip = address['zip']
    if 'city' in address and address['city'] != '':
        city = address['city']
    if 'country' in address and address['country'] != '':
        country = address['country']


    """Check if exists"""
    cur.execute('select id from address where company = {} and '
                'firstname = {} and '
                'lastname = {} and '
                'street = {} and '
                'housenr = {} and '
                'zip = {} and '
                'city = {} and '
                'country = {};'.format(company,firstname, lastname,street, housenr, zip, city, country))
    row = cur.fetchone()
    if row is not None:
        """Address allready exists"""
        return row['id']
    else:
        """Address not exists"""
        """New Address generated"""
        cur.execute('insert into address'
                    '(company, firstname, lastname, street, housenr, zip, city, country) values '
                    '({}, {} ,{}, {}, {}, {}, {}, {})'.format(company, firstname, lastname, street, housenr, zip, city, country))
        db.commit()
        return cur.lastrowid