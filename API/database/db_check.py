import json
import os.path

class DBChecker:
    filename = 'API/database/schema.json'

    def __init__(self, db):
        print('Check if file "' + self.filename + '" exists: ' + str(os.path.isfile(self.filename)))
        self.db = db

    def init(self):
        #If File exists
        if os.path.isfile(self.filename):
            with open(self.filename) as file:
                #Read file Table by table
                json_data = json.loads(file.read())
                for table in json_data:
                    sqltable = self.getTable(table['table'])

                    if sqltable == None:
                        print('Table "{}" does not exists'.format(table['table']))
                        self.createTable(table['table'], table['columns'])
                    else:
                        for column in table['columns']:
                            self.out(column['name'], column['default'], column['type'], column['special'])
        else:
            print('File not found')

    def createTable(self, tablename, columns):
        cur = self.db.cursor()
        sql = "create table {} (".format(tablename)
        for column in columns:
            sql += "{} {} {} {},".format(column['name'], column['type'], column['default'], column['special'])
        sql = sql[:-1] + ');'
        print(sql)
        cur.execute(sql)

    def getTable(self,tablename):
        cur = self.db.cursor()
        try:
            cur.execute('Describe ' + tablename + ';')
            rows = cur.fetchall()
            json_data = []
            for row in rows:
                print(row);
            return json_data
        except:
            return None

    def out(self, x1, x2, x3, x4):
        print('{0:<30}'.format(x1), '| {0:<20}'.format(x2), '| {0:<30}'.format(x3), '| {0:<50}'.format(x4))


