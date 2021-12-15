
from database_req import create_connection
from database_req import get_application
from database_req import get_applications_custom




con = create_connection('database.db')
#res = get_application(con, 0, json_str=True)
l = ["balance", "duration", "history"]
res = get_applications_custom(con, 0, l)


print(res)


