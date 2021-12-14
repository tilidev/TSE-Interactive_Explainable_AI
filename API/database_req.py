
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
    con.row_factory = sql.Row
    c = con.cursor()
    query = 'SELECT * FROM applicants WHERE id = ' + str(id)
    rows = c.execute(query).fetchall()
    con.commit()
    con.close()
    if json_str:
        rows = json.dumps( [dict(ix) for ix in rows] )
    return rows