import sqlite3 as sql
import json
from typing import List
from constants import *


attribute_constraints = [
    {
        attr_name : AttributeNames.balance,
        type : categorical,
        category : financial_cat,
        values : ['no account', 'no balance', 'below 200 EUR', 'above 200 EUR'], #List[str]
        attr_description : "The current balance of the applicant's checking account (in Euro)"
    },
    {
        attr_name : AttributeNames.duration,
        type : continuous,
        category : loan_cat,
        lower_bound : 4, #float
        upper_bound : 72, #float
        attr_description : "The duration of the loan (in months)"
    },
    {
        attr_name : AttributeNames.history,
        type : categorical,
        category : financial_cat,
        values : ['delay payment of previous loans', 'paid back all previous loans at this bank', 'paid back all previous loans', 'no problem with current loans'],
        attr_description : "How reliably the applicant handled previous or current loans"
    },
    {
        attr_name : AttributeNames.purpose,
        type : categorical,
        category : loan_cat,
        values : ['furniture', 'television', 'used car', 'domestic appliances', 'repair', 'retraining', 'business', 'new car', 'other', 'vacation'],
        attr_description : "What the money from the loan will be used for"
    },
    {
        attr_name : AttributeNames.amount,
        type : continuous,
        category : loan_cat,
        lower_bound : 250,
        upper_bound : 11792.5,
        attr_description : "How much money the applicant wants to lend (in euros)"
    },
    {
        attr_name : AttributeNames.savings,
        type : categorical,
        category : financial_cat,
        values : ['no savings account at this bank', 'below 100 EUR', 'between 100 and 500 EUR', 'between 500 and 1000 EUR', 'above 1000 EUR'],
        attr_description : "Amount of savings at that bank (in euros)"
    },
    {
        attr_name : AttributeNames.employment,
        type : categorical,
        category : personal_cat,
        values : ['unemployed', 'less than 1 year', 'between 1 and 4 years', 'between 4 and 7 years', 'more than 7 years'],
        attr_description : "Duration of current applicant's current employment"
    },
    {
        attr_name : AttributeNames.available_income,
        type : categorical,
        category : financial_cat,
        values : ['less than 20%', 'between 20 and 25%', 'between 25 and 35%', 'more than 35%'],
        attr_description : "Percentage of income that the applicant could use for repaying the loan"
    },
    {
        attr_name : AttributeNames.residence,
        type : categorical,
        category : personal_cat,
        values : ['less than 1 year', 'between 1 and 4 years', ' between 4 and 7 years', 'more than 7 years'],
        attr_description : "How long the applicant has lived in current housing"
    },
    {
        attr_name : AttributeNames.assets,
        type : categorical,
        category : financial_cat,
        values : ['none', 'life insurance', 'car', 'real estate'],
        attr_description : "Other resources the applicant might have"
    },
    {
        attr_name : AttributeNames.age,
        type : continuous,
        category : personal_cat,
        lower_bound : 19,
        upper_bound : 75,
        attr_description : "The age of the loan applicant"
    },
    {
        attr_name : AttributeNames.other_loans,
        type : categorical,
        category : financial_cat,
        values : ['no additional loans', 'at department store', 'at other banks'],
        attr_description : "Other installment plans"
    },
    {
        attr_name : AttributeNames.housing,
        type : categorical,
        category : personal_cat,
        values : ['rent', 'for free','own'],
        attr_description : "Whether the applicant pays rent for housing, owns or lives for free"
    },
    {
        attr_name : AttributeNames.previous_loans,
        type : categorical,
        category : financial_cat,
        values : ['1', '2 or 3', '4 or 5', '6'],
        attr_description : "Number of loans the applicant has already had"
    },
    {
        attr_name : AttributeNames.job,
        type : categorical,
        category : personal_cat,
        values : ['unskilled (non-resident)', 'unskilled (permanent resident)', 'skilled','executive or self-employed'],
        attr_description : "Type of profession"
    },
    {
        attr_name : AttributeNames.other_debtors,
        type : categorical,
        category : loan_cat,
        values : ['none', 'co-applicant', 'guarantor'],
        attr_description : "The AI's recommendation whether the loan application should be approved or rejected"
    },
    {
        attr_name : AttributeNames.people_liable,
        type : categorical,
        category : loan_cat,
        values : ['0 to 2', '3 and more'],
        attr_description : "Indicates how confident the AI is in it's decision. Range is [0, 1]"
    }

    # TODO: fill in the rest of the constraints
    # TODO: use smart lower and upper bounds as they will be important for filtering
]

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
    con.close()
    return result

def get_application(con, ident:int, json_str = False):
    """Returns the application information for the application with the specified id.
    Needs a connection con to the database and the id.
    Result can be returned in json format."""
    if json_str:
        con.row_factory = sql.Row
    c = con.cursor()
    query = 'SELECT * FROM applicants WHERE id = ' + str(ident)
    rows = c.execute(query).fetchall()
    if json_str:
        rows = json.dumps([dict(ix) for ix in rows])
    con.close()
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
    con.close()
    return rows



def create_filter_query(filters):
    """Creates a string for the filter query in sql from a given list of filters in json format."""
    filter_str = " WHERE "
    for i in range(0,len(filters)):
            filter_dict = vars(filters[i])
            print(filter_dict)
            attribute = filter_dict['attr_name']
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
    if (sort == 'id'):
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



