import multiprocessing as mp
from pydantic import BaseModel, Field
from constants import ExplanationType
from typing import Optional
from uuid import UUID

class Task(BaseModel):
    exp_type : ExplanationType
    uid : UUID
    task_info : dict # instance attributes and values, arguments necessary for computation & 
    time_out : Optional[float] = Field(None)


def explanation_worker(in_queue : mp.Queue, out_queue : mp.Queue, exp_fn, *args):
    """Takes one element (a job) out of the input queue (TODO BLOCKING), solves the task
    with the explanation function which takes in the args.
    The result is returned in the output queue."""
    pass