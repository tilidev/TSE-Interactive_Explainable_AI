import os
from importlib_metadata import NullFinder
import uvicorn
import multiprocessing as mp
from tensorflow.keras.models import load_model
import pandas as pd
import pickle

from starlette.status import HTTP_202_ACCEPTED
import json

from typing import Any, Optional, List, Union
from fastapi import FastAPI
from fastapi.params import Body
from task_gen import explanation_worker
from task_gen import Job
from typing import Dict
from uuid import UUID
from constants import *
from models import *
from fastapi.middleware.cors import CORSMiddleware
from database_req import *
from lime_utils import LimeHelper

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

manager = None
num_processes = None
task_queue = None # tasks will be inputted here
results : Dict[UUID, Any] = {} # finished tasks will be inputted here, TODO deleted tasks must be removed after client has received them.
tf_model = load_model("smote_ey.tf")

# This preprocessor was pickled in python 3.8.12.
# It follows the steps from data_loader_ey, except that the preprocessor is returned
preprocessor = pickle.load(open("preproc.pickle", "rb"))

# This is necessary for allowing access to the API from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO move explainers to explanation_worker functions
l = LimeHelper()
l.__init__()

@app.post("/table", response_model=List[InstanceInfo], response_model_exclude_none=True) # second parameter makes sure that unused stuff won't be included in the response
async def table_view(request: TableRequest):
    '''Returns a list of "limit" instances for the table view from a specific offset. Can have filters and chosen attributes.'''
    con = create_connection("database.db")
    attributes = [str]
    for i in request.attributes:
        attributes.append(i.value)
    attributes.append("NN_recommendation")
    attributes.append("NN_confidence")
    attributes = attributes[1:] # TODO Keep this in mind
    table_Response = get_applications_custom(con, request.offset, attributes, request.limit, json_str=True, filters=request.filter, sort = request.sort_by, sort_asc= request.sort_ascending)
    return table_Response

@app.get("/instance/{id}", response_model=InstanceInfo)
async def entire_instance_by_id(id: int):
    '''Returns an entire instance information for the lvl2 view'''
    con = create_connection("database.db")
    output = get_application(con, id, json_str=True)
    return output 

@app.post("/instance/predict", response_model=PredictionResponse) # TODO Make Model specific instance infor, with required attributes TODO make specific response model
async def predict_instance(instance: ModelInstanceInfo):
    """Predict the provided instance using the `smote_ey` tensorflow model. Will return `NN_recommendation` and `NN_confidence`."""
    
    data_dict = {col : [instance.__dict__[rename_dict[col]]] for col in feature_names_model_ordered}
    df = pd.DataFrame(data_dict) # Only works when all attributes are provided correctly
    data_to_predict = preprocessor.transform(df)
    prediction = tf_model.predict(data_to_predict)[0][0] # list in list
    if prediction < 0.5:
        confidence = 1 - prediction
        recommendation = "Approve"
    else:
        confidence = prediction
        recommendation = "Reject"

    res = PredictionResponse(NN_confidence=confidence, NN_recommendation=recommendation)
    return res

@app.get("/attributes/information", response_model=List[Union[CategoricalInformation, ContinuousInformation]], response_model_exclude_none=True)
async def attribute_informations():
    '''Returns a JSON with the constraints for each attribute.'''
    result = json.dumps(attribute_constraints)
    result = json.loads(result)
    return result

@app.post("/explanations/{exp_method}", response_model=ExplanationTaskScheduler, status_code=HTTP_202_ACCEPTED)
async def schedule_explanation_generation(
    instance: InstanceInfo,
    exp_method: ExplanationType,
    num_features: Optional[int] = Body(None, description="<b>LIME</b>: the number of features for the lime computation"),
    is_modified: bool = Body(False, description="<b>DICE</b>: if True, the counterfactuals are not pre-generated and the explanation is computed dynamically"),
    num_cfs: Optional[int] = Body(None, le=15, ge=1, description="<b>DICE</b>: number of counterfactuals")
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

    #TODO: assume that each attribute is in the instance_info, but only if shap and lime!!!
    job = Job(exp_type=exp_method, status=ResponseStatus.in_prog)
    job.task = {"instance" : instance, "num_features" : num_features, "num_cfs" : num_cfs, "is_modified" : is_modified}
    results[job.uid] = job
    task_queue.put(job)

    return ExplanationTaskScheduler(status=ResponseStatus.in_prog, href=str(job.uid))

@app.get("/explanations/lime", response_model=LimeResponse, response_model_exclude_none=True)
async def lime_explanation(uid: UUID):
    '''Returns the <b>LIME</b> explanation results or the status of the processing of the original request (`schedule_explanation_generation`).
    Can be used for <b>LIME</b> lvl 2 as well as lvl 3'''
    if uid in results.keys():
        res = results[uid]
        #TODO delete entry in dictionary
        #TODO make call to check all dict entries
        return LimeResponse(status=ResponseStatus.terminated, values=res)
    else:
        return LimeResponse(status=ResponseStatus.in_prog)

@app.get("/explanations/shap", response_model=ShapResponse, response_model_exclude_none=True)
async def shap_explanation(uid: UUID):
    '''Returns the <b>SHAP</b> explanation results or the status of the processing of the original request (`schedule_explanation_generation`).
    Can be used for <b>SHAP</b> lvl 2 as well as lvl 3'''

    if uid in results.keys():
        res = results[uid]
        #TODO delete entry in dictionary
        #TODO make call to check all dict entries
        return res
    else:
        return ShapResponse(status=ResponseStatus.in_prog)

@app.get("/explanations/dice", response_model=DiceCounterfactualResponse, response_model_exclude_none=True)
async def dice_explanation(process_id: int):
    '''Returns the counterfactuals for the request or the status of the processing of the original request (`schedule_explanation_generation`).'''
    pass

@app.get("/processes")
async def processes():
    """Return the number of child explanation processes started by the application."""
    return num_processes

@app.post("/experiment/creation", status_code=HTTP_202_ACCEPTED)
async def create_experiment(exp_info : ExperimentInformation):
    """Create an experiment setup and save it to the database"""
    #check legal boolean combination
    if exp_info.iswhatif:
        if exp_info.ismodify == False:
            #TODO should some error be thrown?
            return
    exp = exp_info.json()
    con = create_connection('database.db')
    exp_creation(con, exp_info.experiment_name, exp)

@app.get("/experiment/all", response_model=List[str])
async def experiment_list():
    """Returns a list of all experiment names, which can be used to access specific experiments."""
    con = create_connection('database.db')
    return get_all_exp(con) 

@app.get("/experiment", response_model=ExperimentInformation)
async def experiment_by_name(name: str):
    """Returns the experiment setup associated to the experiment name."""
    con = create_connection('database.db')
    return get_exp_info(con, name)

@app.post("/experiment/generate_id", response_model=ClientIDResponse)
async def generate_client_id(gen: GenerateClientID):
    con = create_connection('database.db')
    return create_id(con, gen.experiment_name)

@app.post("/experiment/results", status_code=HTTP_202_ACCEPTED)
async def results_to_database(results: ExperimentResults):
    con = create_connection('database.db')
    add_res(con, results.experiment_name, results.client_id, results.results)

@app.get("/experiment/results/export", response_model=List[ExperimentResults])
async def export_results(format: ExportFormat):
    con = create_connection('database.db')
    return export_results_to(con, format.value)

@app.post("/experiment/reset")
async def reset_experiment_results(experiment_name: str):
    con = create_connection('database.db')
    reset_exp_res(con, experiment_name)
    # TODO what would be the best response model?

@app.post("/experiment/delete")
async def delete_experiment(experiment_name: str):
    con = create_connection('database.db')
    delete_exp(con, experiment_name)
    # TODO what would be the best response model

if __name__ == "__main__":
    # This is needed for multiprocessing to run correctly on windows

    num_processes = mp.cpu_count() - 2 # will raise NotImplementedError if count cannot be determined
    manager = mp.Manager()
    results = manager.dict()
    task_queue = manager.Queue()

    print(f"\nMain process with id {os.getpid()} started succesfully. Starting {num_processes} explainer processes.\n")
    processes : List[mp.Process] = [mp.Process(target=explanation_worker, args=(task_queue, results)) for _ in range(num_processes)]
    for process in processes:
        process.start()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

    for process in processes:
        pid = process.pid
        process.terminate()
        print(f"\nSuccesfully terminated explainer process with id {pid}")