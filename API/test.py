
from database_req import create_connection
from database_req import get_application
from database_req import get_applications_custom
from database_req import create_order_query
import json




con = create_connection('database.db')
#res = get_application(con, 0, json_str=True)
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
filters = [filter1, filter2]
res = get_applications_custom(con, 0, l, sort='balance')
print(res)

