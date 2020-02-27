import pyodbc
import pandas as pd


class SQLConnection():
    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};\
                            Server=pacific-ica.cvb4dklzq2km.us-west-1.rds.amazonaws.com, 1433;\
                            Database=db_pacific_ica;uid=admin;pwd=Animal05')
        print("Database Connection Established")

    def closeConnection(self):
        self.conn.close()

    def loginUser(self, userName, password):
        sql = """
            SELECT
                Users.Password,
                Users.PersonnelId,
                Users.ActiveInd,
                Users.Role,
                Users.Email
            FROM
                Users
            WHERE
                Users.UserName = ?"""
        
        
        #print(sql)
        data = pd.read_sql(sql, self.conn, params={userName})
        if data.empty:
            return
        data = data.values.tolist()
        #print(data.head())
        if data[0][0] == password:
            return User([data[0][1],"First Name", "Last Name", data[0][2], data[0][3], data[0][4]], 1)
        else:
            return None
        

def select(column, table):
    # build connection with the database

    conn = pyodbc.connect('Driver={SQL Server};\
                            Server=pacific-ica.cvb4dklzq2km.us-west-1.rds.amazonaws.com, 1433;\
                            Database=db_pacific_ica;uid=admin;pwd=Animal05')

    # cursor = conn.cursor()
    print("connected")

    sql = "SELECT "+column+" FROM " + table
    data = pd.read_sql(sql, conn)
    # conn.commit()-- save any changes to the database

    # print results

    # send sql query
    #"""sql = '''
    #SELECT *
    #FROM table_1
    #'''
    #cursor.execute(sql)

    #for row in cursor:
    #    print(row)"""

    conn.close()
    return data


print(select("PatientID", "Patient"))

def main():
    myConnection = SQLConnection()
    d = myConnection.loginUser("b32206b5f729b815087f8dbf236ddffe8fe511c267750c1d8fcd64b04454e83c","f691b6ef9c9150e03b3b8584f3ca18956fd886374defe65f480bd1c2511eba33")
    myConnection.closeConnection()
    print(d)
main()
