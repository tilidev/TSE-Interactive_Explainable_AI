import sqlite3 as sql
import json

def create_connection(db):
    con = None
    try:
        con = sql.connect(db)
    except sql.Error as e:
        print(e)
    return con


def get_applications(con, start, num = 10):
    c = con.cursor()
    end = int(start) + int(num)
    query = 'SELECT * FROM applicants WHERE id >= ' + str(start) + ' AND id < ' + str(end)  
    c.execute(query)
    result = c.fetchall()
    return result

def get_application(con, id, json_str = False):
    c = con.cursor()
    query = 'SELECT * FROM applicants WHERE id = ' + str(id)
    rows = c.execute(query).fetchall()
    if json_str:
        con.row_factory = sql.Row
        rows = json.dumps([dict(ix) for ix in rows])
    return rows


def get_applications_custom(con, start, attributes,  num = 10, json_str = False):   
    c = con.cursor()
    chosen = ''
    if len(attributes) > 0:
        for i in range(0,len(attributes)):
            chosen += str(attributes[i])
            chosen += ','
        chosen = chosen[:-1]
    end = int(start) + int(num)
    query = 'SELECT ' + chosen + ' FROM applicants WHERE id >= ' + str(start) + ' AND id < ' + str(end) 
    rows = c.execute(query).fetchall()
    if json_str:
        con.row_factory = sql.Row
        rows = json.dumps([dict(ix) for ix in rows])
    return rows

