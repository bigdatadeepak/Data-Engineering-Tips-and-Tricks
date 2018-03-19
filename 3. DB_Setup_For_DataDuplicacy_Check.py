import sqlite3
import os.path as path

present_path =  path.realpath(__file__)
input_path = path.join(path.dirname(path.dirname(path.dirname(present_path))),"data\\input")
db_path = path.join(path.dirname(path.dirname(path.dirname(present_path))),"data\\project_DB\\File_processing_History.db")
try:
    db = sqlite3.connect(db_path)
    with db:
        db.execute('''CREATE TABLE IF NOT EXISTS
                      audit_table(file_id TEXT PRIMARY KEY, file_name TEXT)''')
        db.execute('''INSERT INTO audit_table(file_id,file_name)
                  VALUES(?,?)''', ('DUMMY', 'DUMMY'))
except sqlite3.IntegrityError:
    print('Record already exists')