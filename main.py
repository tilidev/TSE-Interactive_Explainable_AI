from typing import Any, Optional, List, Union
from fastapi import FastAPI
from fastapi.params import Body, Query
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.schema import schema
from enum import Enum

app = FastAPI()

# string and number definitions to re-use through the entire code
row_limit = 20

type = "type"
values = "values"
categorical = "categorical"
continuous = "continuous"
lower_bound = "lower_bound"
upper_bound = "upper_bound"


class AttributeNames(str, Enum):
    '''This class is used to have a central definition of how the attributes are referenced'''

    # attributes in the dataset
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

    # meta-attributes
    id = "id"
    NN_recommendation = "NN_recommendation"
    NN_confidence = "NN_confidence"

category_mapping = {
    "financial" : [AttributeNames.history, AttributeNames.savings, AttributeNames.balance, AttributeNames.available_income, AttributeNames.assets, AttributeNames.other_loans, AttributeNames.other_debtors, AttributeNames.previous_loans],
    "personal" : [AttributeNames.age, AttributeNames.job, AttributeNames.housing, AttributeNames.residence, AttributeNames.employment],
    "loan" : [AttributeNames.amount, AttributeNames.duration, AttributeNames.purpose, AttributeNames.people_liable]
}

attribute_constraints = {
    # TODO: can all of this be done with Field() or schema() ??
    AttributeNames.balance : {
        type : categorical,
        values : [] #List[str]
    },
    AttributeNames.duration : {
        type : continuous,
        lower_bound : 0, #float
        upper_bound : 1 #float
    },
    AttributeNames.history : {
        type : categorical,
        values : [] 
    },
    AttributeNames.purpose : {
        type : categorical,
        values : []
    },
    AttributeNames.amount : {
        type : continuous,
        lower_bound : 0,
        upper_bound : 1
    },
    AttributeNames.savings : {
        type : categorical,
        values : []
    },
    AttributeNames.employment : {
        type : categorical,
        values : []
    },
    AttributeNames.available_income : {
        type : categorical,
        values : []
    },
    AttributeNames.residence : {
        type : categorical,
        values : []
    },
    AttributeNames.assets :{
        type : categorical,
        values : []
    },
    AttributeNames.age : {
        type : continuous,
        lower_bound : 16,
        upper_bound : 100
    },
    AttributeNames.other_loans : {
        type : categorical,
        values : []
    },
    AttributeNames.housing : {
        type : categorical,
        values : []
    },
    AttributeNames.previous_loans : {
        type : categorical,
        values : []
    },
    AttributeNames.job : {
        type : categorical,
        values : []
    },
    AttributeNames.other_debtors : {
        type : categorical,
        values : []
    },
    AttributeNames.people_liable : {
        type : categorical,
        values : []
    }
    # TODO: fill in the rest of the constraints
    # TODO: use smart lower and upper bounds as they will be important for filtering
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
    '''Defines the format for a continuous filter request body'''
    attribute_name: AttributeNames
    lower_bound: float
    upper_bound: float

class CategoricalFilter(BaseModel):
    '''Defines the format for a categorical filter request body'''
    attribute_name: AttributeNames
    values: List[str]

class InstanceInfo(BaseModel):
    '''Defines how a JSON response for an instance information should look like.
    Maps the predefined names for attributes as the alias of the pydantic class keys.'''
    
    # TODO: change the types (most are strings now)
    # TODO: add stuff like ai recommendation and confidence level
    id : Optional[int] = Field(None ,alias=AttributeNames.id.value)
    balance : Optional[str] = Field(None, alias=AttributeNames.balance.value)
    duration : Optional[str] = Field(None, alias=AttributeNames.duration.value)
    history : Optional[str] = Field(None, alias=AttributeNames.history.value)
    purpose : Optional[str] = Field(None, alias=AttributeNames.purpose.value)
    amount : Optional[str] = Field(None, alias=AttributeNames.amount.value)
    savings : Optional[str] = Field(None, alias=AttributeNames.savings.value)
    employment : Optional[str] = Field(None, alias=AttributeNames.employment.value)
    available_income : Optional[str] = Field(None, alias=AttributeNames.available_income.value)
    residence : Optional[str] = Field(None, alias=AttributeNames.residence.value)
    assets : Optional[str] = Field(None, alias=AttributeNames.assets.value)
    age : Optional[str] = Field(None, alias=AttributeNames.age.value)
    other_loans : Optional[str] = Field(None, alias=AttributeNames.other_loans.value)
    housing : Optional[str] = Field(None, alias=AttributeNames.housing.value)
    previous_loans : Optional[str] = Field(None, alias=AttributeNames.previous_loans.value)
    job : Optional[str] = Field(None, alias=AttributeNames.job.value)
    other_debtors : Optional[str] = Field(None, alias=AttributeNames.other_debtors.value)
    people_liable : Optional[str] = Field(None, alias=AttributeNames.people_liable.value)
    NN_recommendation : Optional[bool] = Field(None, alias=AttributeNames.NN_recommendation.value)
    NN_confidence : Optional[float] = Field(None, le=1, ge=0, alias=AttributeNames.NN_confidence.value)


@app.post("/table", response_model=List[InstanceInfo], response_model_exclude_none=True) # second parameter makes sure that unused stuff won't be included in the response
def table_view(
    filter: Optional[List[Union[ContinuousFilter, CategoricalFilter]]] = None,
    attributes: List[AttributeNames] = standard_attributes,
    sort_by: AttributeNames = Body(AttributeNames.id),
    limit: int = Body(row_limit),
    offset: int = Body(0)
):
    example_result = [
        {
            AttributeNames.amount : 3200,
            AttributeNames.duration : 24,
            AttributeNames.id : 1,
            AttributeNames.age : 23,
            AttributeNames.employment : "between 1 and 4 years",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
        },
        {
            AttributeNames.amount : 8000,
            AttributeNames.duration : 12,
            AttributeNames.id : 2,
            AttributeNames.age : 47,
            AttributeNames.employment : "more than 7 years",
            AttributeNames.NN_recommendation : True,
            AttributeNames.NN_confidence : 0.93
        }
    ]
    return example_result