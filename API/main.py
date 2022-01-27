import os
import uvicorn
import multiprocessing as mp
from tensorflow.keras.models import load_model

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
from database_req import get_applications_custom, create_connection, get_application
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

@app.post("/instance/predict", response_model=InstanceInfo)
async def predict_instance(instance: InstanceInfo):
    """Predict the provided instance using the `SMOTE` tensorflow model. Will return `NN_recommendation` and `NN_confidence`."""
    

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
    job = Job(exp_type=exp_method, status=ResponseStatus.in_prog)
    job.task = {"instance" : instance, "num_features" : num_features, "num_cfs" : num_cfs, "is_modified" : is_modified}
    results[job.uid] = job
    task_queue.put(job)


    return ExplanationTaskScheduler(status=ResponseStatus.in_prog, href=str(job.uid))

    # TODO implement background task generation, queue, etc.

    pass

@app.get("/explanations/lime", response_model=LimeResponse, response_model_exclude_none=True)
async def lime_explanation(process_id: int):
    '''Returns the <b>LIME</b> explanation results or the status of the processing of the original request (`schedule_explanation_generation`).
    Can be used for <b>LIME</b> lvl 2 as well as lvl 3'''
    pass

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
    """Return the number of child processes started by the application."""
    return num_processes

@app.post("/experiment/creation", status_code=HTTP_202_ACCEPTED)
async def create_experiment(exp_info : ExperimentInformation):
    """Create an experiment setup and save it to the database"""
    #TODO check legal boolean combination, check unique name in db, ...
    pass

@app.get("/experiment/all", response_model=List[str])
async def experiment_list():
    """Returns a list of all experiment names, which can be used to access specific experiments."""
    #TODO return list of experiment names
    pass

@app.get("/experiment", response_model=ExperimentInformation)
async def experiment_by_name(name: str):
    """Returns the experiment setup associated to the experiment name."""
    # TODO check if name exists in db, if yes return data
    pass

@app.post("/experiment/generate_id", response_model=ClientIDResponse)
async def generate_client_id(gen: GenerateClientID):
    #TODO create client id based on already existing ids in database. Should be integer from 0 upwards.
    pass

@app.post("experiment/results", status_code=HTTP_202_ACCEPTED)
async def results_to_database(results: ExperimentResults):
    #TODO 
    pass

@app.get("experiment/results/export", response_model=List[ExperimentResults])
async def export_results(format: ExportFormat):
    # TODO
    pass

@app.post("experiment/reset")
async def reset_experiment_results(experiment_name: str):
    # TODO what would be the best response model?
    # TODO check if name in database
    pass

@app.post("experiment/delete")
async def delete_experiment(experiment_name: str):
    # TODO what would be the best response model
    # TODO check if name in db
    pass

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