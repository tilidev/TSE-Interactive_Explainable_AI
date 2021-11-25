from pydantic import BaseModel
from typing import Optional
from enums import AttributeNames
from pydantic.fields import Field

class AttributeDescriptionModel(BaseModel):
    '''Defines how a JSON response for the attribute descriptions should look like.
    Maps the predefined names for attributes as the alias of the pydantic class keys.'''
    
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
    NN_recommendation : Optional[str] = Field(None, alias=AttributeNames.NN_recommendation.value)
    NN_confidence : Optional[str] = Field(None, alias=AttributeNames.NN_confidence.value)