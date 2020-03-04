import pyodbc
import pandas as pd
import Patients 
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
            return Users.User(values, 1, self)
        else:
            return None
    def loadQuerry(self, fileName):
        output = ""
        fp = open("Querries/" + fileName + ".txt", "r")
        for line in fp:
            output = output + line
        return output

    def getDefaultWorkQueue(self):
        sql = self.loadQuerry("default_work_queue")
        
        #print(sql)
        data = pd.read_sql(sql, self.conn)
        if data.empty:
            #print("Empty Data")
            return
        data = data.values.tolist()
        plist = []

        for p in data:
            #print(p)
            plist.append(Patients.Patient(p))
            
        return plist

    def getAllPermissions(self):
        sql = self.loadQuerry("get_all_permissions")

        data = pd.read_sql(sql, self.conn)
        if data.empty:
            #print("Empty Data")
            return
        data = data.values.tolist()
        permissionsList = []

        for p in data:
            permissionsList.append(Users.Permissions(p))
    
        return permissionsList

    def getPermission(self, userType):
        sql = self.loadQuerry("get_permission")

        data = pd.read_sql(sql, self.conn,params={userType})
        if data.empty:
            #print("Empty Data")
            return
        data = data.values.tolist()
        output = Users.Permissions(data[0])
        return output
    
def main():
    SQL = SQLConnection()
    SQL.getPermission("Admin")
if __name__ == "__main__":
    main()
