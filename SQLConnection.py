import pyodbc
import pandas as pd
from Patients import *
import Users



class SQLConnection():
    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};\
                            Server=pacific-ica.cvb4dklzq2km.us-west-1.rds.amazonaws.com, 1433;\
                            Database=db_pacific_ica;uid=admin;pwd=Animal05')
        #print(self.conn)
        print("Database Connection Established")

    def closeConnection(self):
        self.conn.close()

    def loginUser(self, userName, password):
        sql = self.loadQuerry("login_querry")
        
        #print(sql)
        data = pd.read_sql(sql, self.conn, params={userName})
        if data.empty:
            #print("Empty Data")
            return
        data = data.values.tolist()
        values = list([data[0][1],data[0][5], data[0][6], data[0][2], data[0][3], data[0][4]])
        #print(values)
        if data[0][0] == password:
            return Users.User(values, 1)
        else:
            return None
    def loadQuerry(self, fileName):
        output = ""
        fp = open("Querries/" + fileName + ".txt", "r")
        for line in fp:
            output = output + line
        return output
