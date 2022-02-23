from queue import Queue
from pydantic import BaseModel, Field
from models import ShapResponse, LimeResponse
from shap_utils import compute_response_shap
from constants import ResponseStatus, ExplanationType, all_features
from typing import Optional
from uuid import UUID, uuid4
import time

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

class Job(BaseModel):
    exp_type : ExplanationType
    uid : UUID = Field(default_factory=uuid4)
    task : dict = {} # instance attributes with values & arguments necessary for computation
    status : str = Field(ResponseStatus)
    time_out : Optional[float] = Field(None)


def explanation_worker(in_queue : Queue, res_out : dict):
    """Takes one element (a job) out of the input queue (TODO BLOCKING), solves the task
    with the explanation function which takes in the args.
    The result is returned in the output queue.
    
    Params:
    -------
    :param in_queue: the multiprocessing.Manager Queue used for shared memory between processes. Tasks are in here.
    :param res_out: the Manager dict used to store the results of the computations with respect to the Job uuid

    TODO """
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
    # imports for explainers
    # Need to happen in the worker, because pickle can't serialize the necessary objects for child processes

    #Shap
    import shap
    from shap_utils import ShapHelperV2
    sh = ShapHelperV2()
    sh.prepare_shap()
    pred_fn = sh.predict_shap


    shap_explainer = shap.KernelExplainer(pred_fn, sh.X_train)
    cols = sh.X_train.columns.to_list()

    #Lime
    from lime_utils import LimeHelper
    lh = LimeHelper()

    print(f"\033[92mINFO:\033[0m Explainer process with id \033[96m{os.getpid()}\033[0m started succesfully. Explainers loaded and ready.")
    
    while True: # repeat the process
        print(f"\033[92mINFO:\033[0m Explainer process with id \033[96m{os.getpid()}\033[0m is waiting for the next task.")
        job : Job = in_queue.get(block=True) # explicitely wait until a job is available
        start_time = time.time()
        print(f"\033[92mINFO:\033[0m Explainer process with id \033[96m{os.getpid()}\033[0m starting exlanation computation. \
            \n      Explanation type: \033[1m{job.exp_type.value}\033[0m")

        if job.exp_type == ExplanationType.shap:
            shap_bval, shap_vals = compute_response_shap(job.task["instance"], shap_explainer, cols)

            shap_attributes = [{"attribute" : cols[i], "influence" : shap_vals[0][i]} for i in range(len(cols))] # prepare format for response

            out = ShapResponse(status=ResponseStatus.terminated, base_value=shap_bval, values=shap_attributes)
            res_out[job.uid] = out


        elif job.exp_type == ExplanationType.lime:
            if job.task["num_features"] is not None:
                num_features = job.task["num_features"]
            else:
                num_features = all_features

            lh_res = lh.get_lime_values(job.task["instance"].__dict__, num_features) #pass the instance in the required format
            out = lh_res
            res_out[job.uid] = LimeResponse(status=ResponseStatus.terminated, values=lh_res)
        
        end_time = time.time()

        print(f"\033[92mINFO:\033[0m Explainer process with id \033[96m{os.getpid()}\033[0m finished \033[1m{job.exp_type.value}\033[0m computation.\n      Time taken: {end_time-start_time} seconds.")
        print(f"      Result saved with uuid {job.uid}.")


def timeout_explanation(uid: UUID, results_dict: dict):
    '''Will remove the generated explanation a certain amount of time after its generation.'''
    timeout_exp = 300
    time.sleep(timeout_exp)
    timeouted = results_dict.pop(uid)

    print(f"\033[92mINFO:\033[0m Explanation with uuid {uid} has been deleted due to timeout.")   