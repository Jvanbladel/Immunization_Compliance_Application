import datetime

class Permissions():
     def __init__(self, permissionList):
        self.importData = permissionList[0]
        self.exportData = permissionList[1]
        self.viewHistoryOfSelf = permissionList[2]
        self.viewHistoryOfEntireSystem = permissionList[3]
        self.viewSelfAnalytics = permissionList[4]
        self.viewSystemAnalytics = permissionList[5]
        self.createAlerts = permissionList[6]
        self.setPermissions = permissionList[7]
        self.serachEntireDatabase = permissionList[8]
        self.printFiles = permissionList[9]
        self.outReach = permissionList[10]
        self.approveUsers = permissionList[11]
        self.numberOfPatientsOpen = permissionList[12]
        self.goalNumberOfOutReaches = permissionList[13]
        self.setSystemOptions = permissionList[14]
        self.consoleCommands = permissionList[15]

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
    def __init__(self, data, isNewSession):
        
        self.userId = data[0]
        self.userFirstName = data[1]
        self.userLastName = data[2]
        self.activeUser = data[3]
        self.userType = data[4]
        if isNewSession == 1:
            self.currentUserSession = UserSession(self.userId, None)
        #Querry User Permissions Here
        if self.userType == "Admin":
            self.permissions = Permissions([1,1,1,1,1,1,1,1,1,1,1,1,10,100,1,1])
        else:
            self.permissions = Permissions([0,0,1,0,1,0,0,0,1,1,1,0,5,50,0,0])

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
