from starlette.status import HTTP_202_ACCEPTED
import uvicorn

from typing import Any, Dict, Optional, List, Union
from fastapi import FastAPI, status
from fastapi.params import Body
from constants import *
from models import DiceCounterfactualResponse, ExplanationTaskScheduler, InstanceInfo, ContinuousInformation, CategoricalInformation, LimeResponse, ShapResponse, TableRequest
from responses import table_Response
from fastapi.middleware.cors import CORSMiddleware

API_description = '''
# TSE: Explainable Artificial Intelligence - API
## authors: Isabelle Konrad, Felix Hasse, Nicolas Kiefer, Tilio Schulze
___
### API: JSON key naming
To change the key names, go to the file `constants.py`. This API uses the defined strings in
`constants.py` as key aliases. All the `pydantic` models conform to using `pydantic.Field` with the constant strings
as the public aliases. This leads to a better separation between the python naming norms and the API key names.
'''

app = FastAPI(description=API_description)

# This is necessary for allowing access to the API from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# central definition of constraints, attribute type, category and values/bounds
attribute_constraints = [
    {
        attr_name : AttributeNames.balance,
        display_name : "",
        type : categorical,
        category : financial_cat,
        values : [], #List[str]
        attr_description : "The current balance of the applicant's checking account (in Euro)"
    },
    {
        attr_name : AttributeNames.duration,
        display_name : "",
        type : continuous,
        category : loan_cat,
        lower_bound : 0, #float
        upper_bound : 1, #float
        attr_description : "The duration of the loan (in months)"
    },
    {
        attr_name : AttributeNames.history,
        display_name : "",
        type : categorical,
        category : financial_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.purpose,
        display_name : "",
        type : categorical,
        category : loan_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.amount,
        display_name : "",
        type : continuous,
        category : loan_cat,
        lower_bound : 0,
        upper_bound : 1,
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.savings,
        display_name : "",
        type : categorical,
        category : financial_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.employment,
        display_name : "",
        type : categorical,
        category : personal_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.available_income,
        display_name : "",
        type : categorical,
        category : financial_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.residence,
        display_name : "",
        type : categorical,
        category : personal_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.assets,
        display_name : "",
        type : categorical,
        category : financial_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.age,
        display_name : "",
        type : continuous,
        category : personal_cat,
        lower_bound : 16,
        upper_bound : 100,
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.other_loans,
        display_name : "",
        type : categorical,
        category : financial_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.housing,
        display_name : "",
        type : categorical,
        category : personal_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.previous_loans,
        display_name : "",
        type : categorical,
        category : financial_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.job,
        display_name : "",
        type : categorical,
        category : personal_cat,
        values : [],
        attr_description : "..."
    },
    {
        attr_name : AttributeNames.other_debtors,
        display_name : "",
        type : categorical,
        category : loan_cat,
        values : [],
        attr_description : "The AI's recommendation whether the loan application should be approved or rejected"
    },
    {
        attr_name : AttributeNames.people_liable,
        display_name : "",
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
    
    return table_Response


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


@app.post("explanations/{exp_method}", response_model=ExplanationTaskScheduler, status_code=HTTP_202_ACCEPTED)
async def schedule_explanation_generation(
    instance: InstanceInfo,
    exp_method: ExplanationMethod,
    num_features: Optional[int] = Body(None, description="<b>LIME</b>: the number of features for the lime computation"),
    is_modified: bool = Body(False, description="<b>DICE</b>: if True, the counterfactuals are not pre-generated and the explanation is computed dynamically"),
    num_cfs: Optional[int] = Body(None, le=15, ge=1, description="<b>DICE</b>: number of counterfactuals"),
):
    '''General scheduler for any of the xai explanations. As the computations can take a large amount of time, the back-end
    returns the information that the task has been started and returns a reference as well as a process id to check for & return the actual
    explantion. Notice that the front-end has to check periodically for the (status of the) result until its computation has finished.
    Only attributed specific to the explanation method (`exp_method`) will be considered.
    ___
    <h1>LIME</h1>
    The back-end will take at least an `id` for the instance information, so that it can either look up the instance in the database
    or use the attributes in the request body to compute an explanation. For the second option to work, it is vital that the request
    contains each instance-attribute's respective value. (The neural network recommendation and confidence will get ignored if passed in the request)
    Note that this method can thus be used for existing as well as modified instances.
    The query parameter `num_features` is optional and if provided, will execute the <b>LIME</b> explanation with the corresponding number of features.
    It can be used to differentiate between lvl 2 and lvl 3 <b>LIME</b>, if computation time is a concern.
    ___
    <h1>SHAP</h1>
    The back-end will take at least an `id` for the instance information, so that it can either look up the instance in the database
    or use the attributes in the request body to compute an explanation. For the second option to work, it is vital that the request
    contains each instance-attribute's respective value. (The neural network recommendation and confidence will get ignored if passed in the request)
    Note that this method can thus be used for existing as well as modified instances.
    ___
    <h1>DICE</h1>
    Only the modified attributes are set in the response items of the `counterfactuals` list.
    Will look up the precomputed counterfactual explanation if `is_modified` is `False` and the instance `id` is passed.
    If one of the two conditions is not met (e.g. for modified instances), the counterfactual explanation will automatically be computed.
    As this computation process may take a lot of time, the process will be handled in a seperate background process.
    The Front-End should implement some kind of information for the user, that a long computation should be expected. The number of counterfactuals
    is limited to 15
    ___
    <b>Notice</b> that `id` is a required field for the InstanceInfo model. `id` should be the value `-1` if the instance has been modified.
    In that case, the server can handle the explanation generation using the values of the sent attributes.
    If the `id` is known, the back-end can look up the instance in the database and output pre-saved explanations (e.g. <b>DICE</b>)
    '''
    # TODO implement background task generation, queue, etc.
    pass

@app.get("/explanations/lime", response_model=LimeResponse, response_model_exclude_none=True)
async def lime_explanation(process_id: int):
    '''Returns the <b>LIME</b> explanation results or the status of the processing of the original request (`schedule_explanation_generation`).
    Can be used for <b>LIME</b> lvl 2 as well as lvl 3'''
    pass

@app.get("/explanations/shap", response_model=ShapResponse, response_model_exclude_none=True)
async def shap_explanation(process_id: int):
    '''Returns the <b>SHAP</b> explanation results or the status of the processing of the original request (`schedule_explanation_generation`).
    Can be used for <b>SHAP</b> lvl 2 as well as lvl 3'''
    pass

@app.get("/explanations/dice", response_model=DiceCounterfactualResponse, response_model_exclude_none=True)
async def dice_explanation(process_id: int):
    '''Returns the counterfactuals for the request or the status of the processing of the original request (`schedule_explanation_generation`).'''
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)