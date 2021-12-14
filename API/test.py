
from database_req import create_connection
from database_req import get_applications


con = create_connection('database.db')
res = get_applications(con, 0)
print(res)
