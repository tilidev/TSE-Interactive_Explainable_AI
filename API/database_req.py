
import sqlite3 as sql


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