import uvicorn

from typing import Any, Dict, Optional, List, Union
from fastapi import FastAPI
from fastapi.params import Body, Query
from constants import *
from models import InstanceInfo, ContinuousFilter, CategoricalFilter, ContinuousInformation, CategoricalInformation, LimeAttribute, TableRequest

API_description = '''

___
### API: JSON key naming
To change the key names, go to the file `constants.py`. This API uses the defined strings in
`constants.py` as key aliases. All the `pydantic` models conform to using `pydantic.Field` with the constant strings
as the public aliases. This leads to a better separation between the python naming norms and the API key names.
'''

app = FastAPI(description=API_description)


# central definition of constraints, attribute type, category and values/bounds
attribute_constraints = [
    {
        attr_name : AttributeNames.balance,
        type : categorical,
        category : financial_cat,
        values : [], #List[str]
        attr_description : "The current balance of the applicant's checking account (in Euro)"
    },
    {
        attr_name : AttributeNames.duration,
        type : continuous,
        category : loan_cat,
        lower_bound : 0, #float
        upper_bound : 1, #float
        attr_description : "The duration of the loan (in months)"
    },
    {
        attr_name : AttributeNames.history,
        type : categorical,
        category : financial_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.purpose,
        type : categorical,
        category : loan_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.amount,
        type : continuous,
        category : loan_cat,
        lower_bound : 0,
        upper_bound : 1,
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.savings,
        type : categorical,
        category : financial_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.employment,
        type : categorical,
        category : personal_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.available_income,
        type : categorical,
        category : financial_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.residence,
        type : categorical,
        category : personal_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.assets,
        type : categorical,
        category : financial_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.age,
        type : continuous,
        category : personal_cat,
        lower_bound : 16,
        upper_bound : 100,
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.other_loans,
        type : categorical,
        category : financial_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.housing,
        type : categorical,
        category : personal_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.previous_loans,
        type : categorical,
        category : financial_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.job,
        type : categorical,
        category : personal_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.other_debtors,
        type : categorical,
        category : loan_cat,
        values : [],
        attr_description : "The AI's recommendation whether the loan application should be approved or rejected"
    },
    {
        attr_name : AttributeNames.people_liable,
        type : categorical,
        category : loan_cat,
        values : [],
        attr_description : "Indicates how confident the AI is in it's decision. Range is [0, 1]"
    }
    # TODO: fill in the rest of the constraints
    # TODO: use smart lower and upper bounds as they will be important for filtering
]

@app.post("/table", response_model=List[InstanceInfo], response_model_exclude_none=True) # second parameter makes sure that unused stuff won't be included in the response
async def table_view(request: TableRequest):
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
async def entire_instance_by_id(id: int):
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
async def attribute_informations():
    '''Returns a JSON with the constraints for each attribute.'''
    return attribute_constraints

@app.post("/explanations/lime", response_model=List[LimeAttribute])
async def lime_explanation_lvl_2(instance: InstanceInfo, num_features: Optional[int] = None):
    '''Defines how the request and response for a <b>LIME</b> explanation call should look like.
    The back-end will take at least an `id` for the instance information, so that it can either look up the instance in the database
    or use the attributes in the request body to compute an explanation. For the second option to work, it is vital that the request
    contains each instance-attribute's respective value. (The neural network recommendation and confidence will get ignored if passed in the request) 
    The query parameter `num_features` is optional and if provided, will execute the <b>LIME</b> explanation with the corresponding number of features.
    It can be used to differentiate between lvl 2 and lvl 3 <b>LIME</b>, if computation time is a concern.
    ___
    Notice that `id` is a required field for the InstanceInfo model. `id` should be the value `-1` if the instance has been modified.
    In that case, the server can handle the explanation generation using the values of the sent attributes.
    If the `id` is known, the back-end can look up the instance in the database and output pre-saved explanations (e.g. <b>DICE</b>).'''
    
    pass

@app.get("/explanations/lvl2/shap", response_model=None)
async def shap_explanation_lvl_2():
    pass

@app.get("/explanations/lvl2/dice", response_model=None)
async def dice_explanation_lvl_2():
    pass

@app.get("/explanations/lvl3/shap", response_model=None)
async def shap_explanation_lvl_3():
    pass

@app.get("/explanations/lvl3/dice", response_model=None)
async def dice_explanation_lvl_3():
    pass

# store modified explanation in front-end
@app.post("/explanations/modify")
async def modify_instance():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)