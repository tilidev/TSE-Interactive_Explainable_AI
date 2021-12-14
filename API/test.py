
from database_req import create_connection
from database_req import get_application




con = create_connection('database.db')
res = get_application(con, 0, json_str=True)
print(res)


