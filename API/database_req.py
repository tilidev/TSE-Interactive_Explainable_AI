import sqlite3 as sql
import json
from typing import List

from constants import AttributeNames
from main import attribute_constraints

ordering_info = {
    'ident': 'ORDER BY ident', 
    'balance': 'ORDER BY CASE WHEN balance = "no account" THEN 1 END WHEN balance = "no balance" THEN 2 END WHEN balance = "below 200 EUR" THEN 3 END WHEN balance = "above 200 EUR" THEN 4 END', 
    'duration': 'ORDER BY duration',
    'history': 'ORDER BY CASE WHEN history = "delay payment of previous loans" THEN 1 END WHEN history = "paid back all previous loans at this bank" THEN 2 END WHEN history = "paid back all previous loans" THEN 3 END WHEN history = "no problem with current loans" THEN 4 END',
    'purpose': 'ORDER BY CASE WHEN purpose = "furniture" THEN 1 END WHEN purpose = "television" THEN 2 END WHEN purpose = "used car" THEN 3 END WHEN purpose = "domestic appliances" THEN 4 END WHEN purpose = "repair" THEN 5 END WHEN purpose = "retraining" THEN 6 END WHEN purpose = "business" THEN 7 END WHEN purpose = "new car" THEN 8 END WHEN purpose = "other" THEN 9 END WHEN purpose = "vacation" THEN 10 END',
    'amount': 'ORDER BY amount', 
    'savings': 'ORDER BY CASE WHEN savings = "no savings account at this bank" THEN 1 END WHEN savings = "below 100 EUR" THEN 2 END WHEN savings = "between 100 and 500 EUR" THEN 3 END WHEN savings = "between 500 and 1000 EUR" THEN 4 END WHEN savings = "above 1000 EUR" THEN 5 END', 
    'employment': 'ORDER BY CASE WHEN employment = "unemployed" THEN 1 END WHEN employment = "less than 1 year" THEN 2 END WHEN employment = "between 1 and 4 years" THEN 3 END WHEN employment = "between 4 and 7 years" THEN 4 END WHEN employment = "more than 7 years" THEN 5 END', 
    'available_income': 'ORDER BY CASE WHEN available_income = "less than 20%" THEN 1 END WHEN available_income = "between 20 and 25%" THEN 2 END WHEN available_income = "between 25 and 35%" THEN 3 END WHEN available_income = "more than 35%" THEN 4 END', 
    'residence': 'ORDER BY CASE WHEN residence = "less than 1 year" THEN 1 END WHEN residence = "between 1 and 4 years" THEN 2 END WHEN residence = " between 4 and 7 years" THEN 3 END WHEN residence = "more than 7 years" THEN 4 END',
    'assets': 'ORDER BY CASE WHEN assets = "none" THEN 1 END WHEN assets = "life insurance" THEN 2 END WHEN assets = "car" THEN 3 END WHEN assets = "real estate" THEN 4 END', 
    'age': 'ORDER BY age', 
    'other_loans': 'ORDER BY CASE WHEN other_loans = "no additional loans" THEN 1 END WHEN other_loans = "at department store" THEN 2 END WHEN other_loans = "at other banks" THEN 3 END',
    'housing': 'ORDER BY CASE WHEN housing = "rent" THEN 1 END WHEN housing = "for free" THEN 2 END WHEN housing = "own" THEN 3 END', 
    'previous_loans': 'ORDER BY CASE WHEN previous_loans = "1" THEN 1 END WHEN previous_loans = "2 or 3" THEN 2 END WHEN previous_loans = "4 or 5" THEN 3 END WHEN previous_loans = "6" THEN 4 END',
    'job': 'ORDER BY CASE WHEN job = "unskilled (non-resident)" THEN 1 END WHEN job = "unskilled (permanent resident)" THEN 2 END WHEN job = "skilled" THEN 3 END WHEN job = "executive or self-employed" THEN 4 END', 
    'other_debtors': 'ORDER BY CASE WHEN other_debtors = "none" THEN 1 END WHEN other_debtors = "co-applicant" THEN 2 END WHEN other_debtors = "guarantor" THEN 3 END', 
    'people_liable': 'ORDER BY CASE WHEN people_liable = "0 to 2" THEN 1 END WHEN people_liable = "3 and more" THEN 2 END'
}

def create_connection(db: str):
    """ Builds a connection to the database stored in the given file db and returns the connection element."""
    con = None
    try:
        con = sql.connect(db)
    except sql.Error as e:
        print(e)
    return con


def get_applications(con, start:int, num = 20):
    c = con.cursor()
    end = int(start) + int(num)
    query = 'SELECT * FROM applicants WHERE ident >= ' + str(start) + ' AND ident < ' + str(end)  
    c.execute(query)
    result = c.fetchall()
    return result

def get_application(con, ident:int, json_str = False):
    """Returns the application information for the application with the specified id."""
    if json_str:
        con.row_factory = sql.Row
    c = con.cursor()
    query = 'SELECT * FROM applicants WHERE ident = ' + str(ident)
    rows = c.execute(query).fetchall()
    if json_str:
        rows = json.dumps([dict(ix) for ix in rows])
    return rows


def get_applications_custom(con, start:int, attributes: List[str],  num = 20, json_str = False, filters = None, sort = "ident", sort_desc = False):   
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
    end = start + num
    view_query += 'SELECT Row_Number() OVER '
    view_query += ordering_info("'"+sort + "'")
    if sort_desc:
        view_query += 'DESC'
    view_query += ' RowNum,' + chosen + ' FROM applicants'  
     
    #add filters to query
    if filters:
        view_query += " WHERE " + create_filter_query(filters)
    print(view_query)
    c.execute(view_query)
    con.commit()
    query = ''
    #rows = c.execute(query).fetchall()
    #c.execute("DROP VIEW custom")
    #con.commit()
    #if json_str:
    #    rows = json.dumps([dict(ix) for ix in rows])
    #return rows



def create_filter_query(filters):
    filter_str = ""
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
    query = '(ORDER BY '
    attr_dict = {}
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
    query += ')'
    print(query)
    return query

def ordering_info_dict_creation():
    ordering_dict ={'ident':'ORDER BY ident'}
    for i in attribute_constraints:
        query = 'ORDER BY '
        if i['type'] == 'categorical':
            query += 'CASE'
            count = 1
            for j in i['values']:
                query += ' WHEN '+ i['attribute'] + ' = "' + j + '" THEN ' + str(count)
                count += 1
                query += ' END'
        else:
            query += i['attribute']
        ordering_dict[i['attribute']] = query
    return ordering_dict

