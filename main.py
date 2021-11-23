from typing import Any, Optional, List, Union
from fastapi import FastAPI
from fastapi.params import Body, Query
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

row_limit = 20

class AttributeNames(str, Enum):
    '''This class is used to have a central definition of how the attributes are referenced'''

    balance = "balance"
    duration = "duration"
    history = "history"
    purpose = "purpose"
    amount = "amount"
    savings = "savings"
    employment = "employment"
    available_income = "available_income"
    #status_sex = "status_sex"
    residence = "residence"
    assets = "assets"
    age = "age"
    other_loans = "other_loans"
    housing = "housing"
    previous_loans = "previous_loans"
    job = "job"
    #telephone = "telephone"
    #foreign_worker = "foreign_worker"
    other_debtors = "other_debtors"
    people_liable = "people_liable"
    id = "id"

category_mapping = {
    "financial" : [AttributeNames.history, AttributeNames.savings, AttributeNames.balance, AttributeNames.available_income, AttributeNames.assets, AttributeNames.other_loans, AttributeNames.other_debtors, AttributeNames.previous_loans],
    "personal" : [AttributeNames.age, AttributeNames.job, AttributeNames.housing, AttributeNames.residence, AttributeNames.employment],
    "loan" : [AttributeNames.amount, AttributeNames.duration, AttributeNames.purpose, AttributeNames.people_liable]
}

attribute_constraints = {
    AttributeNames.balance : {
        "type" : "categorical",
        "values" : [] #List[str]
    },
    AttributeNames.duration : {
        "type" : "continuous",
        "lower_bound" : 0, #float
        "upper_bound" : 1 #float
    }
    # hier noch Rest einfügen
}

# standard configuration for table view
standard_attributes = [
    AttributeNames.amount,
    AttributeNames.duration,
    AttributeNames.balance,
    AttributeNames.age,
    AttributeNames.employment
]

class ContinuousFilter(BaseModel):
    attribute_name: AttributeNames
    lower_bound: float
    upper_bound: float

class CategoricalFilter(BaseModel):
    attribute_name: AttributeNames
    values: List[str]

@app.post("/table")
def table_view(filter: Optional[List[Union[ContinuousFilter, CategoricalFilter]]] = None, attributes: List[AttributeNames] = standard_attributes, sort_by: AttributeNames = Body(AttributeNames.id), limit: int = Body(row_limit), offset: int = Body(0)):
    return attributes