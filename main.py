from typing import Any, Dict, Optional, List, Union
from fastapi import FastAPI
from fastapi.params import Body, Query
from pydantic import BaseModel
from pydantic.fields import Field
from constants import *
from models import AttributeDescription, InstanceInfo, ContinuousFilter, CategoricalFilter, ContinuousConstraint, CategoricalConstraint

app = FastAPI()

category_mapping = {
    "financial" : [AttributeNames.history, AttributeNames.savings, AttributeNames.balance, AttributeNames.available_income, AttributeNames.assets, AttributeNames.other_loans, AttributeNames.other_debtors, AttributeNames.previous_loans],
    "personal" : [AttributeNames.age, AttributeNames.job, AttributeNames.housing, AttributeNames.residence, AttributeNames.employment],
    "loan" : [AttributeNames.amount, AttributeNames.duration, AttributeNames.purpose, AttributeNames.people_liable]
}

attribute_constraints = [
    {
        attr_name : AttributeNames.balance,
        type : categorical,
        values : [] #List[str]
    },
    {
        attr_name : AttributeNames.duration,
        type : continuous,
        lower_bound : 0, #float
        upper_bound : 1 #float
    },
    {
        attr_name : AttributeNames.history,
        type : categorical,
        values : [] 
    },
    {
        attr_name : AttributeNames.purpose,
        type : categorical,
        values : []
    },
    {
        attr_name : AttributeNames.amount,
        type : continuous,
        lower_bound : 0,
        upper_bound : 1
    },
    {
        attr_name : AttributeNames.savings,
        type : categorical,
        values : []
    },
    {
        attr_name : AttributeNames.employment,
        type : categorical,
        values : []
    },
    {
        attr_name : AttributeNames.available_income,
        type : categorical,
        values : []
    },
    {
        attr_name : AttributeNames.residence,
        type : categorical,
        values : []
    },
    {
        attr_name : AttributeNames.assets,
        type : categorical,
        values : []
    },
    {
        attr_name : AttributeNames.age,
        type : continuous,
        lower_bound : 16,
        upper_bound : 100
    },
    {
        attr_name : AttributeNames.other_loans,
        type : categorical,
        values : []
    },
    {
        attr_name : AttributeNames.housing,
        type : categorical,
        values : []
    },
    {
        attr_name : AttributeNames.previous_loans,
        type : categorical,
        values : []
    },
    {
        attr_name : AttributeNames.job,
        type : categorical,
        values : []
    },
    {
        attr_name : AttributeNames.other_debtors,
        type : categorical,
        values : []
    },
    {
        attr_name : AttributeNames.people_liable,
        type : categorical,
        values : []
    }
    # TODO: fill in the rest of the constraints
    # TODO: use smart lower and upper bounds as they will be important for filtering
]

# standard configuration for table view
standard_attributes = [
    AttributeNames.amount,
    AttributeNames.duration,
    AttributeNames.balance,
    AttributeNames.age,
    AttributeNames.employment
]

@app.post("/table", response_model=List[InstanceInfo], response_model_exclude_none=True) # second parameter makes sure that unused stuff won't be included in the response
def table_view(
    filter: Optional[List[Union[ContinuousFilter, CategoricalFilter]]] = None,
    attributes: List[AttributeNames] = standard_attributes,
    sort_by: AttributeNames = Body(AttributeNames.ident),
    limit: int = Body(row_limit),
    offset: int = Body(0)
):
    '''Returns a list of "limit" instances for the table view from a specific offset. Can have filters and chosen attributes.'''
    
    example_result = [
        {
            AttributeNames.amount : 3200,
            AttributeNames.duration : 24,
            AttributeNames.ident : 1,
            AttributeNames.age : 23,
            AttributeNames.employment : "between 1 and 4 years",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
        },
        {
            AttributeNames.amount : 8000,
            AttributeNames.duration : 12,
            AttributeNames.ident : 2,
            AttributeNames.age : 47,
            AttributeNames.employment : "more than 7 years",
            AttributeNames.NN_recommendation : True,
            AttributeNames.NN_confidence : 0.93
        }
    ]
    return example_result


@app.get("/instance/{id}", response_model=InstanceInfo)
def get_entire_instance_by_id(id: int):
    '''Returns an entire instance information for the lvl2 view'''
    example_output = {
        AttributeNames.amount : 8000,
        AttributeNames.duration : 12,
        AttributeNames.assets : "example_value",
        AttributeNames.available_income : "example_value" ,
        AttributeNames.ident : id,
        AttributeNames.age : 47,
        AttributeNames.employment : "more than 7 years",
        AttributeNames.NN_recommendation : True,
        AttributeNames.NN_confidence : 0.93
    }
    return example_output 

@app.get("/attribute/constraints", response_model=List[Union[CategoricalConstraint, ContinuousConstraint]])
def get_attribute_constraints():
    '''Returns a JSON with the constraints for each attribute.'''
    return attribute_constraints

@app.get("attributes/descriptions", response_model=List[AttributeDescription])
def get_attribute_descriptions():
    example_output = {
        AttributeNames.balance : "The current balance of the applicant's checking account (in Euro)",
        AttributeNames.duration : "The duration of the loan (in months)",
        AttributeNames.history : "...",
        AttributeNames.purpose : "...",
        AttributeNames.amount : "...",
        AttributeNames.savings : "...",
        AttributeNames.employment : "...",
        AttributeNames.available_income : "...",
        AttributeNames.other_debtors : "...",
        AttributeNames.residence : "...",
        AttributeNames.assets : "...",
        AttributeNames.age : "...",
        AttributeNames.other_loans : "...",
        AttributeNames.housing : "...",
        AttributeNames.previous_loans : "...",
        AttributeNames.job : "...",
        AttributeNames.people_liable : "...",
        AttributeNames.NN_recommendation : "The AI's recommendation whether the loan application should be approved or rejected",
        AttributeNames.NN_confidence : "Indicates how confident the AI is in it's decision",
    }
    return example_output