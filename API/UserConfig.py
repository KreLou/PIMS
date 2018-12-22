from API.db import get_db


def getConfig():
    db = get_db()
    cur = db.cursor()
    cur.execute('select maxPackageAge from settings where settingsID = 1;')
    row = cur.fetchone()

    if row is not None:
        data = {
            'maxPackageAge': row[0]
        }
        return data;
    return None