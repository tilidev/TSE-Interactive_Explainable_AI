from fastapi.params import Body
from pydantic import BaseModel, Field
from typing import Optional, List, Union

from constants import * 

class InstanceInfo(BaseModel):
    '''Defines how a JSON response for an instance information should look like.
    Maps the predefined names for attributes as the alias of the pydantic class keys.'''
    
    # TODO: change the types (most are strings now)
    ident : int = Field(alias=AttributeNames.ident.value, ge=-1, le=1000)
    balance : Optional[str] = Field(None, alias=AttributeNames.balance.value)
    duration : Optional[float] = Field(None, alias=AttributeNames.duration.value)
    history : Optional[str] = Field(None, alias=AttributeNames.history.value)
    purpose : Optional[str] = Field(None, alias=AttributeNames.purpose.value)
    amount : Optional[float] = Field(None, alias=AttributeNames.amount.value)
    savings : Optional[str] = Field(None, alias=AttributeNames.savings.value)
    employment : Optional[str] = Field(None, alias=AttributeNames.employment.value)
    available_income : Optional[str] = Field(None, alias=AttributeNames.available_income.value)
    residence : Optional[str] = Field(None, alias=AttributeNames.residence.value)
    assets : Optional[str] = Field(None, alias=AttributeNames.assets.value)
    age : Optional[float] = Field(None, alias=AttributeNames.age.value)
    other_loans : Optional[str] = Field(None, alias=AttributeNames.other_loans.value)
    housing : Optional[str] = Field(None, alias=AttributeNames.housing.value)
    previous_loans : Optional[str] = Field(None, alias=AttributeNames.previous_loans.value)
    job : Optional[str] = Field(None, alias=AttributeNames.job.value)
    other_debtors : Optional[str] = Field(None, alias=AttributeNames.other_debtors.value)
    people_liable : Optional[str] = Field(None, alias=AttributeNames.people_liable.value)
    NN_recommendation : Optional[bool] = Field(None, alias=AttributeNames.NN_recommendation.value)
    NN_confidence : Optional[float] = Field(None, le=1, ge=0, alias=AttributeNames.NN_confidence.value)

class ContinuousFilter(BaseModel):
    '''Defines the JSON format for a continuous filter request body'''
    attr_name: AttributeNames = Field(alias=attr_name)
    lower_bound: float = Field(alias=lower_bound)
    upper_bound: float = Field(alias=upper_bound)

class CategoricalFilter(BaseModel):
    '''Defines the JSON format for a categorical filter request body'''
    attr_name: AttributeNames = Field(alias=attr_name)
    values: List[str] = Field(alias=values)

class TableRequest(BaseModel):
    filter: Optional[List[Union[ContinuousFilter, CategoricalFilter]]] = Field(None, alias=filter)
    attributes: List[AttributeNames] = Field(standard_attributes, alias=attributes)
    sort_by: AttributeNames = Field(AttributeNames.ident, alias=sort_by)
    limit: int = Field(row_limit, alias=limit)
    offset: int = Field(0, alias=offset)

class CategoricalInformation(BaseModel):
    '''Defines the JSON format for the constraints of a categorical attribute'''
    attr_name: AttributeNames = Field(alias=attr_name)
    type: str = Field(const=categorical, alias=type)
    category: str = Field(alias=category)
    values: List[str]
    description: str = Field(alias=attr_description)

class ContinuousInformation(BaseModel):
    '''Defines the JSON format for the constraints of a categorical attribute'''
    attr_name: AttributeNames = Field(alias=attr_name)
    type: str = Field(const=continuous, alias=type)
    category: str = Field(alias=category)
    lower_bound: float = Field(alias=lower_bound)
    upper_bound: float = Field(alias=upper_bound)
    description: str = Field(alias=attr_description)

class LimeAttribute(BaseModel):
    '''Defines the JSON format for a lime explanation response'''
    attr_name : AttributeNames = Field(alias=attr_name)
    influence : float = Field(alias=influence)
    positive_influence: bool = Field(alias=positive_influence)