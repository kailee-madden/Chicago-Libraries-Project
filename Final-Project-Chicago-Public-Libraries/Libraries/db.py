#!/usr/bin/env python
'''Tools for working with Chicago public library databse'''

import os
import sys
import json
import sqlite3
import argparse


def dict_factory(cursor, row):
    '''strict dictionary format for rows'''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class LibrariesDB(object):
    '''A connection to the libraries database'''
      
    def __init__(self, data_dir):
        '''A new connection to the database'''
        
        self.db_file = os.path.join(data_dir, "libraries.db")
        self.data_file = os.path.join(data_dir, "libs.json")
        self.conn = sqlite3.connect(self.db_file)

        self.conn.row_factory = dict_factory
        self._create_table()
        self._populate_table()
        
    
    
    def _create_table(self):
        '''Create the new tables'''

        # TODO
        cur = self.conn.cursor()
        cur.execute('''DROP TABLE IF EXISTS Library''')

        create_library = '''CREATE TABLE IF NOT EXISTS Library(
        library_id      INTEGER PRIMARY KEY,
        name            TEXT,
        hours           TEXT,
        address         TEXT,
        city            TEXT,
        state           TEXT,
        zipcode        TEXT,
        phone_number    INTEGER,
        website         TEXT,
        teacher_available TEXT
         )'''

        cur.execute(create_library)

        cur = self.conn.cursor()

    
    
    def _populate_table(self):
        '''Populate the table from the json file'''
        
        # TODO 
        cur = self.conn.cursor()
        
        with open(self.data_file) as fh:
            data = json.load(fh)
            
            insert_sql = '''
                INSERT INTO Library VALUES (
                    NULL,
                   :name,
                   :hours,
                   :address,
                   :city,
                   :state,
                   :zip,
                   :phone,
                   :url,
                   :teacher_in_lib
                )'''

            for rec in data:
                rec['url'] = rec['url'][0]
                cur.execute(insert_sql, rec)


        
        self.conn.commit()
    
    
    def search(self, library_name):
        '''Return libraries matching name'''

        cur = self.conn.cursor()
        
        # sql statement
        
        sql = '''SELECT * FROM Library WHERE (name LIKE ?) ORDER BY 
            name'''
        for query in [library_name, library_name + '%', library_name[0] +'%', '%']:
            # I cut this out: '%' + library_name + '%',
            cur.execute(sql, (query,))
            result = cur.fetchall()
            if len(result) > 0:
                break
        return result
    
    
    def detail(self, library_id):
        '''Return one row based on exact match of library_id'''
        
        # TODO
        cur = self.conn.cursor()
        sql = '''SELECT * FROM Library WHERE library_id = ?'''

        cur.execute(sql, (library_id,))
        return cur.fetchone()



        
# main code block: test the module
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'test the LibrariesDB interface'
    )
    parser.add_argument('--name', default='%', help="Value for library")
    parser.add_argument('--data', default='data', help="Path to data directory")
    args = parser.parse_args()
    db = LibrariesDB(args.data)
    
    print json.dumps(db.search(args.name), indent=1)