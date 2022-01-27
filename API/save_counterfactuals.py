import dice_ml
import pandas as pd
from tensorflow.python.keras.saving.save import load_model
from DataLoader_ey import data_loader
import tensorflow as tf
import json
from multiprocessing import Process, Queue

def process_instance(query_instance, exp):
    dice_exp = exp.generate_counterfactuals(query_instance, total_CFs=5, desired_class="opposite", posthoc_sparsity_algorithm="binary")
    cf_result = json.loads(dice_exp.to_json())['cfs_list']
    return cf_result

def iterate_instances(start, num_instances, data: pd.DataFrame, exp, queue, no_queue=False):
    result = {}
    for i in range(start, start + num_instances):
        instance = data.iloc[i, :].to_dict()
        result[i] = process_instance(instance, exp)
    
    if no_queue:
        return result

    queue.put(result)


if __name__ == "__main__":
    # This part works, but I have yet to figure out how to do it with multiprocessing, because of some pickle error
    # Some cfs take 3 minutes to load, which means this could take a very huge amount of time...
    m_processes = 4
    instances_per_process = 2

    data = data_loader('Data/german.csv')

    backend = 'TF2'
    model = load_model('smote_ey.tf')
    d = dice_ml.Data(dataframe=data, continuous_features=['duration_', 'amount_', 'age_'], outcome_name='label')
    d.normalize_data(d.one_hot_encode_data(data))
    m = dice_ml.Model(model=model, backend=backend)
    exp = dice_ml.Dice(d, m)
    res = iterate_instances(0, 3, data, exp, None, no_queue=True)

    with open("test_res.json", 'w') as f: # This would be the end file in which everything is saved
        json.dump(res, f)
        
    





if __name__ == "test": # old code do not delete yet
    num_processes = 4
    instances_per_process = 2

    data = data_loader('Data/german.csv')

    backend = 'TF2'
    model = load_model('smote_ey.tf')
    d = dice_ml.Data(dataframe=data, continuous_features=['duration_', 'amount_', 'age_'], outcome_name='label')
    d.normalize_data(d.one_hot_encode_data(data))
    m = dice_ml.Model(model=model, backend=backend)
    exp = dice_ml.Dice(d, m)

    processes = []
    queue = Queue()

    for i in range(4):
        processes.append(Process(target=iterate_instances, args=(i*instances_per_process, instances_per_process, data, exp, queue)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    end_result = [queue.get() for _ in processes]

    print(end_result[0][1])
    print(end_result[1][3])