from unittest import result
from starlette.status import HTTP_202_ACCEPTED
import json

from typing import Optional, List, Union
from fastapi import FastAPI
from fastapi.params import Body
from constants import *
from models import DiceCounterfactualResponse, ExplanationTaskScheduler, InstanceInfo, ContinuousInformation, CategoricalInformation, LimeResponse, ShapResponse, TableRequest
from fastapi.middleware.cors import CORSMiddleware
from database_req import get_applications_custom, create_connection, get_application

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

# TODO Load the explainers here


# central definition of constraints, attribute type, category and values/bounds
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

@app.post("/table", response_model=List[InstanceInfo], response_model_exclude_none=True) # second parameter makes sure that unused stuff won't be included in the response
async def table_view(request: TableRequest):
    '''Returns a list of "limit" instances for the table view from a specific offset. Can have filters and chosen attributes.'''
    con = create_connection("database.db")
    attributes = [str]
    for i in request.attributes:
        attributes.append(i.value)
    attributes = attributes[1:] # TODO Keep this in mind
    #attributes.append(AttributeNames.NN_recommendation.value)
    #attributes.append(AttributeNames.NN_confidence.value)
    table_Response = get_applications_custom(con, request.offset, attributes, request.limit, json_str=True, filters=request.filter, sort = request.sort_by, sort_asc= request.sort_ascending)
    return table_Response


@app.get("/instance/{id}", response_model=InstanceInfo)
async def entire_instance_by_id(id: int):
    '''Returns an entire instance information for the lvl2 view'''
    con = create_connection("database.db")
    output = get_application(con, id, json_str=True)
    return output 

@app.get("/attributes/information", response_model=List[Union[CategoricalInformation, ContinuousInformation]], response_model_exclude_none=True)
async def attribute_informations():
    '''Returns a JSON with the constraints for each attribute.'''
    result = json.dumps(attribute_constraints)
    result = json.loads(result)
    return result


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
    Only attributes specific to the explanation method (`exp_method`) will be considered.
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