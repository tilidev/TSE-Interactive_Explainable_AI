
from matplotlib.font_manager import json_load
from database_req import *
import json


con = create_connection('database.db')
exp_info_dict = {
    'loan_ids' : [1,2,3,4,5],
    'ismodify' : True,
    'iswhatif' : True, # Should only be True if ismodify is also true
    'exp_type' : 'shap',
    'experiment_name' : 'Test experiment'
}
json1 = json.dumps(exp_info_dict)
json_obj = json.loads(json1)
#exp_creation(con, 'Test experiment', json_obj)

delete_exp(con, 'Test experiment')
'''
#res = get_application(con, 0)
l = ["balance", "duration", "history", "amount"]
#res = get_applications_custom(con, 0, l)
balance_dict = {
    "attribute": "balance",
    "values": ["no balance", "no account"]
}
amount_dict = {
    "attribute": "amount",
    "lower_bound": 0,
    "upper_bound": 10000
}
filter1 = json.dumps(balance_dict)
filter2 = json.dumps(amount_dict)
jsonobject = json.loads(filter2)
#print(jsonobject.type())
filters = [filter1, filter2]
#res = get_applications_custom(con, 0, l, sort='id')
res = get_application(con, 1, json_str=True)
#res = res[1:-1]
print(res)
'''