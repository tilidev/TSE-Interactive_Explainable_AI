import multiprocessing as mp

def explanation_worker(in_queue : mp.Queue, out_queue : mp.Queue, exp_fn, *args):
    """Takes one element (a job) out of the input queue (TODO BLOCKING), solves the task with the explanation function which takes in the args.
    The result is returned in the output queue."""
    pass