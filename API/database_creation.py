from os import rename
from DataLoader_ey import createDataframeForDB
import sqlite3 as sql
from constants import rename_dict

con = sql.connect('database.db')
c = con.cursor()
#create_query ='CREATE TABLE applicants (id INT, balance TEXT,duration INT,history TEXT,purpose TEXT,amount REAL,savings TEXT,employment TEXT,available_income TEXT,other_debtors TEXT,residence TEXT,assets TEXT,age INT,other_loans TEXT,housing TEXT,previous_loans TEXT,job TEXT,people_liable TEXT,telephone TEXT, NN_recommendation TEXT, NN_confidence REAL)'
#c.execute(create_query)
#con.commit()
df = createDataframeForDB()
df.to_sql('applicants', con, index_label = 'id', if_exists="replace")
for key in rename_dict.keys:
    query = 'ALTER TABLE applicants RENAME COLUMN ' + key + ' TO ' + rename_dict[key] + ';'
    c.execute(query)
con.close()
