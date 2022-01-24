import multiprocessing as mp
from queue import Queue
from pydantic import BaseModel, Field
from shap_utils import compute_response_shap
from constants import ResponseStatus
from constants import ExplanationType
from typing import Optional
from uuid import UUID, uuid4

class Job(BaseModel):
    exp_type : ExplanationType
    uid : UUID = Field(default_factory=uuid4)
    task : dict = {} # instance attributes with values & arguments necessary for computation
    status : str = Field(ResponseStatus)
    result : dict = {} # TODO This should be defined in the response models
    time_out : Optional[float] = Field(None)


def explanation_worker(in_queue : Queue, res_out : dict, explainer_shap, explainer_lime, explainer_dice):
    """Takes one element (a job) out of the input queue (TODO BLOCKING), solves the task
    with the explanation function which takes in the args.
    The result is returned in the output queue.
    
    Params:

    :param in_queue: the multiprocessing.Manager Queue used for shared memory between processes. Tasks are in here.
    TODO """

    while True: # repeat the process
        job : Job = in_queue.get(block=True) # wait until a job is available

        if job.exp_type == ExplanationType.shap:
            shap_bval, shap_vals = compute_response_shap()
            

    
    