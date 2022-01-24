import multiprocessing as mp
from pydantic import BaseModel, Field
from API.constants import ResponseStatus
from constants import ExplanationType
from typing import Optional
from uuid import UUID, uuid4

class Job(BaseModel):
    exp_type : ExplanationType
    uid : UUID = Field(default_factory=uuid4)
    task : dict # instance attributes with values & arguments necessary for computation
    status : str = Field(ResponseStatus)
    result : dict = None # TODO This should be defined in the response models
    time_out : Optional[float] = Field(None)


def explanation_worker(in_queue, res_out, exp_fn, *args):
    """Takes one element (a job) out of the input queue (TODO BLOCKING), solves the task
    with the explanation function which takes in the args.
    The result is returned in the output queue.
    
    Params:

    :param in_queue: the multiprocessing.Manager Queue used for shared memory between processes. Tasks are in here."""
    pass