import pyodbc
import pandas as pd
import Patients 
import Users
import query_generator
import Type_Check
import datetime



class SQLConnection():
    def __init__(self):

        try:
            self.conn = pyodbc.connect('Driver={SQL Server};\
                            Server=pacific-ica.cvb4dklzq2km.us-west-1.rds.amazonaws.com, 1433;\
                            Database=db_pacific_ica;uid=admin;pwd=Animal05;', timeout = 3)
            print("Database Connection Established")
            self.online = 1
        except:
            print("Database Connection Failed")
            self.online = 0

    def checkConnection(self):
        if self.online == 1:
            return 1
        else:
            try:
                self.conn = pyodbc.connect('Driver={SQL Server};\
                            Server=pacific-ica.cvb4dklzq2km.us-west-1.rds.amazonaws.com, 1433;\
                            Database=db_pacific_ica;uid=admin;pwd=Animal05;', timeout = 3)
                print("Database Connection Established")
                self.online = 1
                return 1
            except:
                print("Database Connection Failed")
                self.online = 0
                return 0

    def closeConnection(self):
        if self.online == 1:
            self.conn.close()

    def loadQuerry(self, fileName):
        output = ""
        fp = open("Querries/" + fileName + ".txt", "r")
        for line in fp:
            output = output + line
        return output

    def loginUser(self, userName, password):
        if self.checkConnection() == 0:
            return -1

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
        if self.checkConnection() == 0:
            return -1

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
        if self.checkConnection() == 0:
            return
        sql = self.loadQuerry("permissions/get_all_permissions")

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
        if self.checkConnection() == 0:
            return
        sql = self.loadQuerry("permissions/get_permission")

        data = pd.read_sql(sql, self.conn,params={userType})
        if data.empty:
            #print("Empty Data")
            return
        data = data.values.tolist()
        output = Users.Permissions(data[0])
        return output

    def deletePermission(self, role):
        if self.checkConnection() == 0:
            return
        sql = self.loadQuerry("permissions/delete_permission")

        self.conn.execute(sql, (role))
        self.conn.commit()

    def addPermission(self, permission):
        if self.checkConnection() == 0:
            return
        sql = self.loadQuerry("permissions/add_permission")

        params=(permission.name,
                permission.description,
                permission.importData,
                permission.exportData,
                permission.viewHistoryOfSelf,
                permission.viewHistoryOfEntireSystem,
                permission.viewSelfAnalytics,
                permission.viewSystemAnalytics,
                permission.createAlerts,
                permission.setPermissions,
                permission.serachEntireDatabase,
                permission.printFiles,
                permission.outReach,
                permission.approveUsers,
                permission.setSystemOptions,
                permission.consoleCommands,
                permission.numberOfPatientsOpen,
                permission.goalNumberOfOutReaches)
        
        self.conn.execute(sql,params)
        self.conn.commit()

    def addPermission(self, permission):
        if self.checkConnection() == 0:
            return
        sql = self.loadQuerry("permissions/add_permission")

        params=(permission.name,
                permission.description,
                permission.importData,
                permission.exportData,
                permission.viewHistoryOfSelf,
                permission.viewHistoryOfEntireSystem,
                permission.viewSelfAnalytics,
                permission.viewSystemAnalytics,
                permission.createAlerts,
                permission.setPermissions,
                permission.serachEntireDatabase,
                permission.printFiles,
                permission.outReach,
                permission.approveUsers,
                permission.setSystemOptions,
                permission.consoleCommands,
                permission.numberOfPatientsOpen,
                permission.goalNumberOfOutReaches)
        
        self.conn.execute(sql,params)
        self.conn.commit()

    def addUser(self, newUser):
        if self.checkConnection() == 0:
            return
        sql = self.loadQuerry("get_users")
        data = pd.read_sql(sql, self.conn)
        data = data.values.tolist()[0][0]
        #print(data)
        
        sql = self.loadQuerry("add_user")

        params=(data, #personalID
                newUser[0], #first name
                newUser[1], #last name
                newUser[3], #hashed user Name
                newUser[4], #hashed password
                "Y",        #Active ID
                "User",     #Role
                newUser[2], #email
                datetime.datetime.now(),
                data,
                datetime.datetime.now(),
                data) #update ID

        self.conn.execute(sql,params)
        self.conn.commit()

    def getNotificationList(self, userType):
        pass

    def getDemographics(self, patientId):
        if self.checkConnection() == 0:
            return
        sql = self.loadQuerry("Demographics")
        data = pd.read_sql(sql, self.conn, params={patientId})
        if data.empty:
            return
        data = data.values.tolist()
        return Patients.Demographics(data)

    def getServiceDetails(self, patientId):
        if self.checkConnection() == 0:
            return
        sql = self.loadQuerry("Service_Details")
        data = pd.read_sql(sql, self.conn, params={patientId})
        if data.empty:
            return
        #data = data.values.tolist()
        return data

    def getIndWorkEfficiency(self, userId):
        if self.checkConnection() == 0:
            return
        sql = self.loadQuerry("Individual_Work")
        data = pd.read_sql(sql, self.conn, params={userId})
        if data.empty:
            return
        #data = data.values.tolist()
        return data

    def getWorkEfficiency(self):
        if self.checkConnection() == 0:
            return
        sql = self.loadQuerry("Work_Efficiency")
        data = pd.read_sql(sql, self.conn)
        if data.empty:
            return
        #data = data.values.tolist()
        return data

    def getContactNotes(self, patientId):
        if self.checkConnection() == 0:
            return
        sql = self.loadQuerry("Contact_Notes")
        data = pd.read_sql(sql, self.conn, params={patientId})
        if data.empty:
            return
        data = data.values.tolist()
        #print(data)
        return data

    def addContactNotes(self, notes):
        if self.checkConnection() == 0:
            return
        sql = self.loadQuerry("get_contact_notes_id")
        data = pd.read_sql(sql, self.conn)
        data = data.values.tolist()[0][0]
        print(data)
        
        sql = self.loadQuerry("update_contact_notes")

        params=(data, #OutreachDetailsId
                datetime.datetime.now(), #OutreachDetailCreatedDtTm
                "1", #OutreachDetailsCreatedPrsnlId
                datetime.datetime.now(), #OutreachDetailsDate
                "Contact Notes", #Notetype
                "", #OutreachDetailsMethod
                "", #OutreachDetailsOutcome
                notes[0], #OutreachDetailsNotes
                "",  #OutreachDetailsAttemptNumber
                notes[1])#OutreachDetailsPatientId

        self.conn.execute(sql,params)
        self.conn.commit()

    def getInsurence(self, patientId):
        pass

    def getContact(self, patientId):
        pass

    def getAddress(self, patientId0):
        pass

    def executeQuery(self, query):
        data = pd.read_sql(query, self.conn)
        if data.empty:
            print("Empty Data")
            return
        else:
            return data

def main():
    SQL = SQLConnection()
    SQL.addContactNotes(["Test", 2])
    SQL.closeConnection()
if __name__ == "__main__":
    main()
