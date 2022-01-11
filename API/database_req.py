import sqlite3 as sql
import json
from typing import List
from main import attribute_constraints

def create_connection(db: str):
    """ Builds a connection to the database stored in the given file db and returns the connection element."""
    con = None
    try:
        con = sql.connect(db)
    except sql.Error as e:
        print(e)
    return con


def get_applications(con, start:int, num = 20):
    """Returns the applications with the ids from start to start + num
    Needs a connection con to the database.db (use create_connection) and a start value as int """    
    c = con.cursor()
    end = int(start) + int(num)
    query = 'SELECT * FROM applicants WHERE ident >= ' + str(start) + ' AND ident < ' + str(end)  
    c.execute(query)
    result = c.fetchall()
    return result

def get_application(con, ident:int, json_str = False):
    """Returns the application information for the application with the specified id.
    Needs a connection con to the database and the id.
    Result can be returned in json format."""
    if json_str:
        con.row_factory = sql.Row
    c = con.cursor()
    query = 'SELECT * FROM applicants WHERE ident = ' + str(ident)
    rows = c.execute(query).fetchall()
    if json_str:
        rows = json.dumps([dict(ix) for ix in rows])
    return rows


def get_applications_custom(con, start:int, attributes: List[str],  num = 20, json_str = False, filters = None, sort = "ident", sort_asc = True):   
    """Returns a list of application data from the database that is connected via con. 
    Attributes is the list of chosen attributes, num the amount of applications that is requested, 
    filters a list of jsons with filter information, sort a String of the attribute name to be sorted by sort_desc allows to sort by descending order.
    Result can also be returned in json format."""
    if json_str:
        con.row_factory = sql.Row
    c = con.cursor()
    view_query = 'CREATE VIEW custom AS '
    #add customize values
    chosen = ''
    if len(attributes) > 0:
        for i in range(0,len(attributes)):
            chosen += str(attributes[i])
            chosen += ','
        chosen = chosen[:-1]
    view_query += 'SELECT Row_Number() OVER '
    view_query += create_order_query(sort)
    if sort_asc == False:
        view_query += ' DESC'
    view_query += ') RowNum,' + chosen + ' FROM applicants'  
     
    #add filters to query
    if filters:
        view_query += create_filter_query(filters)
    c.execute(view_query)
    con.commit()
    end = start + num
    query = 'SELECT ' + chosen + ' FROM custom WHERE RowNum > ' + str(start) + ' AND RowNum <= ' + str(end)
    rows = c.execute(query).fetchall()
    c.execute("DROP VIEW custom")
    con.commit()
    if json_str:
        rows = json.dumps([dict(ix) for ix in rows])
    return rows



def create_filter_query(filters):
    """Creates a string for the filter query in sql from a given list of filters in json format."""
    filter_str = " WHERE "
    for i in range(0,len(filters)):
            filter_dict = json.loads(filters[i])
            attribute = filter_dict["attribute"]
            if ("values" in filter_dict):
                #categorical filter
                selected = filter_dict["values"]
                filter_str += "("
                for j in range(0,len(selected)):
                    filter_str += attribute + " = " + "'"+ selected[j] + "'"
                    if j < len(selected) - 1:
                        filter_str += " OR "
                filter_str += ")"
            else:
                #numerical
                filter_str += "(" + attribute + " >= " + str(filter_dict["lower_bound"]) + " AND " + attribute + " <= " + str(filter_dict["upper_bound"]) + ")"
            if i < len(filters) - 1:
                filter_str += " AND "
    return filter_str


def create_order_query(sort:str):
    """Creates a string for the ordering query in sql for a given attribute name as a string"""
    query = '(ORDER BY '
    attr_dict = {}
    if (sort == 'ident'):
        query += sort 
        return query
    for i in attribute_constraints:
        if i['attribute'] == sort:
            attr_dict = i
            break
    if (attr_dict['type'] == 'categorical'):
        query += 'CASE'
        count = 1
        for i in attr_dict['values']:
            query += " WHEN "+ sort + " = '" + i + "' THEN " + str(count)
            count += 1
        query += ' END'
    else:
        query += sort
    return query



