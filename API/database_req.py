import sqlite3 as sql
import json

def create_connection(db):
    con = None
    try:
        con = sql.connect(db)
    except sql.Error as e:
        print(e)
    return con


def get_applications(con, start, num = 20):
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


def get_applications_custom(con, start, attributes,  num = 20, json_str = False, filters = None):   
    c = con.cursor()
    #add customize values
    chosen = ''
    if len(attributes) > 0:
        for i in range(0,len(attributes)):
            chosen += str(attributes[i])
            chosen += ','
        chosen = chosen[:-1]
    end = int(start) + int(num)
    query = 'SELECT ' + chosen + ' FROM applicants WHERE id >= ' + str(start) + ' AND id < ' + str(end)  
     
    #add filters to query
    filterStr = ''
    if filters:
        for i in range(0,len(filters)):
            filter_dict = json.loads(filters[i])
            attribute = filter_dict["attribute"]
            if ("values" in filter_dict):
                #categorical filter
                selected = filter_dict["values"]
                filterStr += "("
                for j in selected:
                    filterStr += attribute + " = " + selected[j]
                    if j < len(selected) - 1:
                        filterStr += " OR "
                filterStr += ")"
            else:
                #numerical
                filterStr += "(" + attribute + " >= " + filter_dict["lower_bound"] + " AND " + attribute + " <= " + filter_dict["upper_bound"] + ")"
            if i < len(filters) - 1:
                filterStr += " AND "
        query += "AND " + filterStr

    rows = c.execute(query).fetchall()
    if json_str:
        con.row_factory = sql.Row
        rows = json.dumps([dict(ix) for ix in rows])
    return rows

