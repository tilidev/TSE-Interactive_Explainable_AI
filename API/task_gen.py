import multiprocessing as mp
from queue import Queue
from pydantic import BaseModel, Field
from models import ShapResponse
from shap_utils import compute_response_shap
from constants import ResponseStatus
from constants import ExplanationType
from typing import Optional
from uuid import UUID, uuid4

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

class Job(BaseModel):
    exp_type : ExplanationType
    uid : UUID = Field(default_factory=uuid4)
    task : dict = {} # instance attributes with values & arguments necessary for computation
    status : str = Field(ResponseStatus)
    time_out : Optional[float] = Field(None)


def explanation_worker(in_queue : Queue, res_out : dict, explainer_lime=None): # currently, dice explainer is not needed due to precomputation
    """Takes one element (a job) out of the input queue (TODO BLOCKING), solves the task
    with the explanation function which takes in the args.
    The result is returned in the output queue.
    
    Params:

    :param in_queue: the multiprocessing.Manager Queue used for shared memory between processes. Tasks are in here.
    TODO """
    # imports need to happen here, beause pickle can't do it in any other way
    import shap
    from shap_utils import ShapHelperV2
    sh = ShapHelperV2()
    sh.prepare_shap()
    pred_fn = sh.please_work

    shap_explainer = shap.KernelExplainer(pred_fn, sh.X_train)
    cols = sh.X_train.columns.to_list()

    print(f"\nExplainer process with id {os.getpid()} started succesfully. Explainers loaded and ready.\n")
    
    while True: # repeat the process
        job : Job = in_queue.get(block=True) # explicitely wait until a job is available

        if job.exp_type == ExplanationType.shap:
            if job.task["num_features"] is not None:
                num_features = job.task["num_features"]
            shap_bval, shap_vals = compute_response_shap(job.task["instance"], shap_explainer, cols)

            shap_attributes = [{"attribute" : cols[i], "influence" : shap_vals[0][i]} for i in range(len(cols))] # prepare format for response

            out = ShapResponse(status=ResponseStatus.terminated, base_value=shap_bval, values=shap_attributes)
            res_out[job.uid] = out
            

    
    