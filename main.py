from typing import Optional, List
from fastapi import FastAPI
from fastapi.params import Query
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class AttributeNames(str, Enum):
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

class Filter(BaseModel):
    attribute_name: AttributeNames


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


@app.get("/table")
def table_view(filter: Optional[List[str]] = Query(None), limit: int = 20, offset: int = 0, attributes: List[AttributeNames] = Query(standard_attributes), sort_by: AttributeNames = AttributeNames.id):
    # TODO: filter zur Query machen
    pass
