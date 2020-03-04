import datetime
import SQLConnection

class Permissions():
     def __init__(self, permissionList):
        self.name = permissionList[0]
        self.description = permissionList[1]
        self.importData = permissionList[2]
        self.exportData = permissionList[3]
        self.viewHistoryOfSelf = permissionList[4]
        self.viewHistoryOfEntireSystem = permissionList[5]
        self.viewSelfAnalytics = permissionList[6]
        self.viewSystemAnalytics = permissionList[7]
        self.createAlerts = permissionList[8]
        self.setPermissions = permissionList[9]
        self.serachEntireDatabase = permissionList[10]
        self.printFiles = permissionList[11]
        self.outReach = permissionList[12]
        self.approveUsers = permissionList[13]
        self.numberOfPatientsOpen = permissionList[14]
        self.goalNumberOfOutReaches = permissionList[15]
        self.setSystemOptions = permissionList[16]
        self.consoleCommands = permissionList[17]

class UserAction():
    def __init__(self, actionType, data):
        self.actionTime = str(datetime.datetime.now())
        self.actionType = actionType
        self.acionID = data[0]
        self.data = data[1]

class UserSession():
    def __init__(self, userId, data):
        self.userId = userId
        if data == None:
            self.sessionID = self.createUniqueSessionID()
            self.UserLogin = str(datetime.datetime.now())
            self.UserActionList = []
            self.Userlogout = None
        else:
            self.sessionID = data[0]
            self.UserLogin = data[1]
            self.UserActionList = data[2]
            self.Userlogout = data[3]

    def createUniqueSessionID(self):
        #To DO
        return 12345

    def addAction(self, action):
        self.UserActionList.append(action)

    def endSession(self):
        self.Userlogout = str(datetime.datetime.now())


class UserHistory():
    def __init__(self, history):
        self.UserSessions = history

    def getSession(self, sessionID):
        for session in self.UserSessions:
            if session.sessionID == sessionID:
                return session
        return None

    def addSession(self, session):
        self.UserSessions.append(session)

#History Classes End

class User():
    def __init__(self, data, isNewSession, SQL):
        
        self.userId = data[0]
        self.userFirstName = data[1]
        self.userLastName = data[2]
        self.activeUser = data[3]
        self.userType = data[4]
        if isNewSession == 1:
            self.currentUserSession = UserSession(self.userId, None)
        #Querry User Permissions Here
        self.permissions = SQL.getPermission(self.userType)

    def addAction(self, action):
        self.currentUserSession.addAction(action)

    def getHistoy(self):

        #querry history
        return UserHistory(None)

    def endSession(self):
        self.currentUserSession.endSession()

        #send self.currentUserSession to database

        return 1

    def getHistory(self):
        self.history = UserHistory(userId)
        return
