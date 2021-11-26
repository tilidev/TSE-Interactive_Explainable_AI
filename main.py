from typing import Any, Dict, Optional, List, Union
from fastapi import FastAPI
from fastapi.params import Body, Query
from constants import *
from models import AttributeDescription, InstanceInfo, ContinuousFilter, CategoricalFilter, ContinuousInformation, CategoricalInformation, LimeAttribute

app = FastAPI()

# central definition of constraints, attribute type, category and values/bounds
attribute_constraints = [
    {
        attr_name : AttributeNames.balance,
        type : categorical,
        category : financial_cat,
        values : [], #List[str]
        description : "The current balance of the applicant's checking account (in Euro)"
    },
    {
        attr_name : AttributeNames.duration,
        type : continuous,
        category : loan_cat,
        lower_bound : 0, #float
        upper_bound : 1, #float
        description : "The duration of the loan (in months)"
    },
    {
        attr_name : AttributeNames.history,
        type : categorical,
        category : financial_cat,
        values : [],
        description : "..."
    },
    {
        attr_name : AttributeNames.purpose,
        type : categorical,
        category : loan_cat,
        values : [],
        description : "..."
    },
    {
        attr_name : AttributeNames.amount,
        type : continuous,
        category : loan_cat,
        lower_bound : 0,
        upper_bound : 1,
        description : "..."
    },
    {
        attr_name : AttributeNames.savings,
        type : categorical,
        category : financial_cat,
        values : [],
        description : "..."
    },
    {
        attr_name : AttributeNames.employment,
        type : categorical,
        category : personal_cat,
        values : [],
        description : "..."
    },
    {
        attr_name : AttributeNames.available_income,
        type : categorical,
        category : financial_cat,
        values : [],
        description : "..."
    },
    {
        attr_name : AttributeNames.residence,
        type : categorical,
        category : personal_cat,
        values : [],
        description : "..."
    },
    {
        attr_name : AttributeNames.assets,
        type : categorical,
        category : financial_cat,
        values : [],
        description : "..."
    },
    {
        attr_name : AttributeNames.age,
        type : continuous,
        category : personal_cat,
        lower_bound : 16,
        upper_bound : 100,
        description : "..."
    },
    {
        attr_name : AttributeNames.other_loans,
        type : categorical,
        category : financial_cat,
        values : [],
        description : "..."
    },
    {
        attr_name : AttributeNames.housing,
        type : categorical,
        category : personal_cat,
        values : [],
        description : "..."
    },
    {
        attr_name : AttributeNames.previous_loans,
        type : categorical,
        category : financial_cat,
        values : [],
        description : "..."
    },
    {
        attr_name : AttributeNames.job,
        type : categorical,
        category : personal_cat,
        values : [],
        description : "..."
    },
    {
        attr_name : AttributeNames.other_debtors,
        type : categorical,
        category : loan_cat,
        values : [],
        description : "The AI's recommendation whether the loan application should be approved or rejected"
    },
    {
        attr_name : AttributeNames.people_liable,
        type : categorical,
        category : loan_cat,
        values : [],
        description : "Indicates how confident the AI is in it's decision"
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

@app.get("/attributes/information", response_model=List[Union[CategoricalInformation, ContinuousInformation]])
def get_attribute_constraints():
    '''Returns a JSON with the constraints for each attribute.'''
    return attribute_constraints

@app.get("explanations/lvl2/lime", response_model=List[LimeAttribute])
def lime_explanation_lvl_2():
    pass

@app.get("explanations/lvl2/shap", response_model=None)
def shap_explanation_lvl_2():
    pass

@app.get("explanations/lvl2/dice", response_model=None)
def dice_explanation_lvl_2():
    pass

@app.get("explanations/lvl3/lime", response_model=None)
def lime_explanation_lvl_3():
    pass

@app.get("explanations/lvl3/shap", response_model=None)
def shap_explanation_lvl_3():
    pass

@app.get("explanations/lvl3/dice", response_model=None)
def dice_explanation_lvl_3():
    pass

# use session ids or something like that --> don't compute everything twice!!
@app.post("explanations/modify")
def modify_instance():
    pass