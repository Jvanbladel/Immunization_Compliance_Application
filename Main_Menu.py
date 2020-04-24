import ICA_super
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk,Image
import datetime
import math
from Patients import *
from Med_Info_Screen import *
import Login_Screen
import sort
from Users import *

class mainMenu(ICA_super.icaSCREENS):

    def __init__(self,window, user):
        self.user = user
        super().__init__(window)
        #setUpWindow
        self.root.geometry("800x600")
        menu = Menu(self.root)
        self.root.title("Immunization Compliance Application " + self.versionNumber)

        self.bindKey("<Escape>",self.logOut)

        self.clockUpdater = None
        

        #Max windows open
        self.currentPopOut = 0

        #Set Up  Top Bar
        self.notificationFRAME = LabelFrame(self.root)
        self.notificationFRAME.place(x=0,y=0,height=100,width=800)
        barFRAME = LabelFrame(self.root)
        barFRAME.place(x=0,y=0,height=30,width=800)

        #Add Name/date to top bar
        self.userName = self.user.userFirstName + " " + self.user.userLastName
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        userInfo = self.userName + " " + str(current_time)
        self.userFRAME = Label(self.root,text=userInfo,anchor=E, justify=RIGHT)
        self.userFRAME.place(x=572.5,y=2.5,height=25,width=225)

        #Add tabs to top bar
        self.setUpTabs()

        #set up all screens
        self.mainMenuSCREEN  = 0
        self.consoleSCREEN = 0
        self.permissionsSCREEN = 0
        self.aboutUsSCREEN = 0
        self.guideSCREEN = 0
        self.alertSCREEN = 0
        
        self.showMainMenu()


        #Notifications based on user in future
        self.setUpNotifications([[3,"Very Important Message!"],[2,"Important Message."],[1,"Notification Message"]])


        #update current time
        self.logout = 0
        self.clock()



    def showMainMenu(self):
        self.clearAllScreens()

        #set Up Search Frame
        self.setUpSearchFrame()

        #setUp FilterFrame
        self.filter = 0

        #set Up Queue Frame
        self.setUpQueue()
        self.largeQueue = 0
        self.queue = self.createQueue()
        self.togExpandQueue()

        #SetUpSummary Frame
        self.infoDisplayFRAME = LabelFrame(self.root)
        self.infoDisplayFRAME.place(x=575,y=100,height=500,width=225)
        self.summary = 0
        self.contact = 0
        self.phistory = 0

        #setupOutReach
        self.reportingFRAME = LabelFrame(self.root)
        self.reportingFRAME.place(x=575,y=400,height=200,width=225)
        self.outreach = 0

        self.mainMenuSCREEN  = 1


    def clearAllScreens(self):
        self.closeALLTabs()
        if self.mainMenuSCREEN == 1:
            self.clearPatient()
            self.infoDisplayFRAME.destroy()
            self.reportingFRAME.destroy()

            self.toggleSearchBox()
            if self.filter == 1:
                self.togFilter()

            if not self.myframe == None:
                self.myframe.destroy()
                self.canvas.destroy()
                self.myscrollbar.destroy()
                self.frame.destroy()
                self.scrollHeadFRAME.destroy()
                self.headLABEL.destroy()

            if self.outreach == 1:
                self.reportText.destroy()
                self.outreachText.destroy()
                self.outreachText2.destroy()
                self.callOptions.destroy()
                self.NotesTextArea.destroy()
                self.NotesScrollBar.destroy()
                self.submittOutReach.destroy()
                self.outreach = 0

            self.mainMenuSCREEN  = 0

        if self.consoleSCREEN == 1:
            self.Consolecanvas.destroy()
            self.Consoleframe.destroy()
            self.ConsolemyscrollbarY.destroy()
            self.ConsolemyscrollbarX.destroy()
            self.excuteConsoleBUTTON.destroy()
            self.commandInputENTRY.destroy()
            self.Consolemyframe.destroy()

            for commandLabel in self.consoleCommandList:
                commandLabel.destroy()

            self.consoleSCREEN = 0

        if self.permissionsSCREEN == 1:
            self.Permissionmyframe.destroy()
            self.Permissioncanvas.destroy()
            self.Permissionframe.destroy()
            self.PermissionmyscrollbarY.destroy()
            self.permissionLabelFRAME.destroy()
            self.permissionEditFrame.destroy()
            self.permissionEditMainLabel.destroy()

            self.permissionEditNameField.destroy()
            self.permissionEditNameFieldLabel.destroy()
            self.permissionEditDescriptionFieldLabel.destroy()
            self.permissionEditDescriptionField.destroy()
            self.permissionImportData.destroy()
            self.permissionExportData.destroy()
            self.permissionPersonalHistoryData.destroy()
            self.permissionSystemHistoryData.destroy()
            self.permissionPersonalAnalyticsData.destroy()
            self.permissionSystemAnalyticsData.destroy()
            self.permissionCreateAlertsData.destroy()
            self.permissionSetPermissionsData.destroy()
            self.permissionSearchDatabaseData.destroy()
            self.permissionPrintData.destroy()
            self.permissionOutreachData.destroy()
            self.permissionApproveUsers.destroy()
            self.permissionSystemSettings.destroy()
            self.permissionConsoleCommands.destroy()
            self.permissionsPatientsOpenText.destroy()
            self.permissionsPatientsOpen.destroy()
            self.permissionsGoalNumberOfOutreachesText.destroy()
            self.permissionsGoalNumberOfOutreaches.destroy()
            self.changePermissionBUTTON.destroy()


            self.permissionsSCREEN = 0
            
        if self.guideSCREEN == 1:
            self.guideSCREEN = 0

        if self.aboutUsSCREEN == 1:
            self.aboutUsSCREEN = 0

        if self.alertSCREEN ==1:
            self.alertSCREEN = 0

    def showConsole(self):
        self.clearAllScreens()

        self.Consolemyframe=Frame(self.root,relief=GROOVE,width=20,height=470,bd=1)
        self.Consolemyframe.place(x=0,y=100,height=470,width=800)

        self.Consolecanvas=Canvas(self.Consolemyframe)
        self.Consoleframe=Frame(self.Consolecanvas)
        self.ConsolemyscrollbarY=Scrollbar(self.Consolemyframe,orient="vertical",command=self.Consolecanvas.yview)
        self.Consolecanvas.configure(yscrollcommand=self.ConsolemyscrollbarY.set)
        self.ConsolemyscrollbarY.pack(side="right",fill="y")

        self.ConsolemyscrollbarX=Scrollbar(self.Consolemyframe,orient="horizontal",command=self.Consolecanvas.xview)
        self.Consolecanvas.configure(xscrollcommand=self.ConsolemyscrollbarX.set)
        self.ConsolemyscrollbarX.pack(side="bottom",fill="x")


        self.Consolecanvas.pack(side="left")
        self.Consolecanvas.create_window((0,0),window=self.Consoleframe,anchor='nw')
        self.Consoleframe.bind("<Configure>", self.Consolemyfunction)

        self.commandInputENTRY = Entry(self.root, font = ('Consolas', 10))
        self.commandInputENTRY.place(x=0,y=570,width=750, height = 30)
        self.commandInputENTRY.insert(0, ">> ")

        self.excuteConsoleBUTTON = Button(self.root, text = "Execute", command=lambda: self.executeConsoleCommand())
        self.excuteConsoleBUTTON.place(x=750,y=570, height = 30, width = 50)

        self.consoleCommandList = []
        self.consoleSCREEN = 1

    def Permissionmyfunction(self,event):
        self.Permissioncanvas.configure(scrollregion=self.Permissioncanvas.bbox("all"),width=400,height=475)

    def Consolemyfunction(self,event):
        self.commandInputENTRY.delete(0, END)
        self.commandInputENTRY.insert(0, ">> ")
        self.Consolecanvas.configure(scrollregion=self.Consolecanvas.bbox("all"),width=800,height=570)

    def executeConsoleCommand(self):
        self.addToConsole( self.commandInputENTRY.get())

    def addToConsole(self, commandStr):
        toAddToConsole = Label(self.Consoleframe, text = commandStr,anchor=W, justify=LEFT, font = ('Consolas', 10))
        toAddToConsole.pack(side=TOP, fill=BOTH, expand=TRUE)
        self.consoleCommandList.append(toAddToConsole)

    def exitICA(self): #prompt user if they want to close program

        userChoice = messagebox.askyesno("Exiting ICA","Are you sure you want to exit ICA?")

        if userChoice:
            self.logoutofApp()
            self.root.destroy()

    def setUpNotifications(self, notifications):
        self.notificationList = []

        imageSource = "sources/notifications/notification_1.PNG"
        notificationImage = Image.open(imageSource)
        notificationImage = notificationImage.resize((18,18), Image.ANTIALIAS)
        self.notificationIMAGE1 = ImageTk.PhotoImage(notificationImage)
        imageSource = "sources/notifications/notification_2.PNG"
        notificationImage = Image.open(imageSource)
        notificationImage = notificationImage.resize((18,18), Image.ANTIALIAS)
        self.notificationIMAGE2 = ImageTk.PhotoImage(notificationImage)
        imageSource = "sources/notifications/notification_3.PNG"
        notificationImage = Image.open(imageSource)
        notificationImage = notificationImage.resize((18,18), Image.ANTIALIAS)
        self.notificationIMAGE3 = ImageTk.PhotoImage(notificationImage)

        for n in range(len(notifications)):
            if notifications[n][0] == 1:
                notificationLABEL = Label(self.root,image=self.notificationIMAGE1)
                notificationLABEL.place(x=2.5,y= 32.5 + (n * 20))
                notificationLABEL1 = Label(self.root, text = notifications[n][1])
                notificationLABEL1.place(x=25,y= 32.5 + (n * 20))
                self.notificationList.append(notificationLABEL)
                self.notificationList.append(notificationLABEL1)
            if notifications[n][0] == 2:
                notificationLABEL = Label(self.root,image=self.notificationIMAGE2)
                notificationLABEL.place(x=2.5,y= 32.5 + (n * 20))
                notificationLABEL1 = Label(self.root, text = notifications[n][1])
                notificationLABEL1.place(x=25,y= 32.5 + (n * 20))
                self.notificationList.append(notificationLABEL)
                self.notificationList.append(notificationLABEL1)
            if notifications[n][0] == 3:
                notificationLABEL = Label(self.root,image=self.notificationIMAGE3)
                notificationLABEL.place(x=2.5,y= 32.5 + (n * 20))
                notificationLABEL1 = Label(self.root, text = notifications[n][1])
                notificationLABEL1.place(x=25,y= 32.5 + (n * 20))
                self.notificationList.append(notificationLABEL)
                self.notificationList.append(notificationLABEL1)

    def toggleOutReach(self, patient):
        if self.outreach == 0:


            self.reportText = Label(self.root, text = "Outreach Report")
            self.reportText.place(x=580,y=402.5)
        
            self.outreachText = Label(self.root, text = "Outcome:")
            self.outreachText.place(x=580,y=430)

            self.outreachText2 = Label(self.root, text = "Notes:")
            self.outreachText2.place(x=580,y=455)
        
            contactOptions=("Answered", "Missed Call", "Hung Up", "Will Call Back", "No Number on File", "Wrong Number", "Attempt Again Later")
            self.callOptions=Combobox(self.root, values=contactOptions)
            self.callOptions.place(x=655,y=430, width = 130)

            self.NotesTextArea = Text()
            self.NotesScrollBar = Scrollbar(self.root)
            self.NotesScrollBar.config(command=self.NotesTextArea.yview)
            self.NotesTextArea.config(yscrollcommand=self.NotesScrollBar.set)
            self.NotesScrollBar.place(x=772.5,y=475, height = 90, width = 20)
            self.NotesTextArea.place(x=582.5,y=475, height = 90, width = 190)

            self.submittOutReach = Button(self.root, text = "Submit",command=lambda: self.submitOutReachAttempt(patient))
            self.submittOutReach.place(x= 745, y=567.5)
            self.outreach = 1

        else:
            self.reportText.destroy()
            self.outreachText.destroy()
            self.outreachText2.destroy()
            self.callOptions.destroy()
            self.NotesTextArea.destroy()
            self.NotesScrollBar.destroy()
            self.submittOutReach.destroy()


            self.outreach = 0


    def submitOutReachAttempt(self, patient):
        if self.user.permissions.outReach == 0:
            return
        print("Out Reach", patient.fName)

        #clear patient from queue


        b = self.currentButton

        self.showPatient(patient.MRN, b)

        self.bList.remove(b)
        b.destroy()

        self.resetWorkQueue(patient.MRN)


    def setUpTabs(self):
        fileBUTTON = Button(self.root,text="File",command=lambda: self.togFileTab())
        fileBUTTON.place(x=0,y=0,height=30,width=50)

        optionsBUTTON = Button(self.root,text="Options",command=lambda: self.togOptionsTab())
        optionsBUTTON.place(x=50,y=0,height=30,width=50)

        reportBUTTON = Button(self.root,text="Reports",command=lambda: self.togReportTab())
        reportBUTTON.place(x=100,y=0,height=30,width=50)

        helpBUTTON = Button(self.root,text="Help",command=lambda: self.togHelpTab())
        helpBUTTON.place(x=150,y=0,height=30,width=50)

        currentX = 200
        if not self.user.permissions == None:
            if self.user.permissions.viewSelfAnalytics == 1 or self.user.permissions.viewSystemAnalytics == 1:
                self.analyticTABX = currentX
                analyticBUTTON = Button(self.root,text="Analytics",command=lambda: self.togAnalyticsTab())
                analyticBUTTON.place(x=currentX,y=0,height=30,width=60)
                currentX = currentX + 60

            if self.user.permissions.viewHistoryOfSelf == 1 or self.user.permissions.viewHistoryOfEntireSystem == 1:
                self.historyTABX = currentX
                historyButton = Button(self.root,text="History",command=lambda: self.togHistoryTab())
                historyButton.place(x=currentX,y=0,height=30,width=50)
                currentX = currentX + 50

            if self.user.permissions.approveUsers == 1 or self.user.permissions.setPermissions == 1 or self.user.permissions.createAlerts == 1 or self.user.permissions.createAlerts == 1 or self.user.permissions.consoleCommands == 1:
                self.adminTABX = currentX
                adminBUTTON = Button(self.root,text="Admin",command=lambda: self.togAdminTab())
                adminBUTTON.place(x=currentX,y=0,height=30,width=50)
                currentX = currentX + 50

        #Set Up for TABS
        self.fileFRAME = None
        self.optionFRAME = None
        self.reportFRAME = None
        self.helpFRAME = None
        self.adminFRAME = None
        self.analyticsFRAME = None
        self.logout = None
        self.permissions = None
        self.systemOptions = None
        self.accountManager = None
        self.aboutUs = None
        self.guide = None
        self.print = None
        self.export =  None
        self.exportFRAME = None
        self.pdf = None
        self.txt = None
        self.cvs = None
        self.pName = None
        self.importData = None
        
        #TABS
        self.file = 0
        self.option = 0
        self.report = 0
        self.help = 0
        self.admin = 0
        self.analytics = 0
        self.history = 0


        #SubTabs
        self.exportTAB = 0
        self.notificationsTABState = 0

        #Tab Pages
        self.accountMangerPage = 0


    def toggleSearchBox(self):
        if self.searchBox == 0:
            self.searchFRAME = LabelFrame(self.root)
            self.searchFRAME.place(x=0,y=100,height=500,width=225)
    
            self.searchTXT = Label(self.root, text = "Search: ")
            self.searchTXT.place(x=2.5,y=120)
        
            self.searchENTRY = Entry(self.root)
            self.searchENTRY.place(x=50,y=120,width=160)

            self.closeSearch = Button(self.root, command=lambda: self.togExpandQueue())
            self.closeSearch.place(x= 211, y=102.5, width = 10, height = 10)

            #Options for first Name
            self.var1 = IntVar()
            self.FnameSearch = Checkbutton(self.root, text="First Name", variable=self.var1)
            self.FnameSearch.place(x=2.5,y=160)

            fNameSearchOptions=("Exact Search", "Ascending", "Descending", "Fuzy Search")
            
            self.fNameCombo=Combobox(self.root, values=fNameSearchOptions)
            self.fNameCombo.place(x=110, y=160, width = 100)

            #Options for last Name
            self.var2 = IntVar()
            self.LnameSearch = Checkbutton(self.root, text="Last Name", variable=self.var2)
            self.LnameSearch.place(x=2.5,y=185)

            lNameSearchOptions=("Exact Search", "Ascending", "Descending", "Fuzy Search")
            
            self.LnameCombo=Combobox(self.root, values=lNameSearchOptions)
            self.LnameCombo.place(x=110, y=185, width = 100)


            #Options for DOB Search
            self.var3 = IntVar()
            self.DOBSearch = Checkbutton(self.root, text="Date of Birth", variable=self.var3)
            self.DOBSearch.place(x=2.5,y=210)

            DOBOptions=("Exact Search", "Ascending", "Descending")
            
            self.DOBCombo=Combobox(self.root, values=DOBOptions)
            self.DOBCombo.place(x=110, y=210, width = 100)
            
            #Options for Due Date
            #self.var3 = IntVar()
            #self.dueDateSearch = Checkbutton(self.root, text="Due Date", variable=self.var3)
            #self.dueDateSearch.place(x=2.5,y=210)

            #dueDateSearchOptions=("Exact Search", "Ascending", "Descending", "Fuzy Search")
            
            #self.fNameCombo=Combobox(self.root, values=dueDateSearchOptions)
            #self.fNameCombo.place(x=110, y=210, width = 100)

            #Options for MRN
            self.var4 = IntVar()
            self.MRNSearch = Checkbutton(self.root, text="MRN", variable=self.var4)
            self.MRNSearch.place(x=2.5,y=235)

            MRNSearchOptions=("Exact Search", "Ascending", "Descending", "Fuzy Search")
            
            self.MRNCombo=Combobox(self.root, values=MRNSearchOptions)
            self.MRNCombo.place(x=110, y=235, width = 100)


            #Options for Immunizations Type
            self.var5 = IntVar()
            self.ImmunTypeSearch = Checkbutton(self.root, text="Immunization", variable=self.var5)
            self.ImmunTypeSearch.place(x=2.5,y=260)

            ImmunTypeSearchOptions=("Vaccine 1", "Vaccine 2", "Vaccine 3", "Vaccine 4")
            
            self.ImmunTypeCombo=Combobox(self.root, values=ImmunTypeSearchOptions)
            self.ImmunTypeCombo.place(x=110, y=260, width = 100)

            #Search Buttons

            self.defaultQueueBUTTON = Button(self.root, text = "Default Work Queue", command=lambda: self.resetQueueToDefault())
            self.defaultQueueBUTTON.place(x=20, y = 290, width = 177.5, height = 25)

            self.searchforBUTTON = Button(self.root, text = "Search",bg="blue",fg="white", command=lambda: self.searchFunc())
            self.searchforBUTTON.place(x=122.5, y = 320, width = 75, height = 32.5)

            self.advancedsearchBUTTON = Button(self.root, text = "More\nOptions", command=lambda: self.togAdvancedSearch())
            self.advancedsearchBUTTON.place(x=20, y = 320, width = 75, height = 32.5)


            self.advancedSearchFRAME = LabelFrame(self.root)
            self.advancedSearchFRAME.place(x=0,y=370,height=230,width=225)
        
            self.searchBox = 1
            self.advancedSearch = 0
        else:
            self.searchFRAME.destroy()
            self.searchTXT.destroy()
            self.searchENTRY.destroy()
            self.closeSearch.destroy()
            self.FnameSearch.destroy()
            self.fNameCombo.destroy()
            self.LnameSearch.destroy()
            self.LnameCombo.destroy()
            self.DOBSearch.destroy()
            self.DOBCombo.destroy()
            self.MRNSearch.destroy()
            self.MRNCombo.destroy()
            self.ImmunTypeSearch.destroy()
            self.ImmunTypeCombo.destroy()
            self.searchforBUTTON.destroy()
            self.advancedsearchBUTTON.destroy()
            self.advancedSearchFRAME.destroy()
            self.defaultQueueBUTTON.destroy()
            if self.advancedSearch == 1:
                self.togAdvancedSearch()
            self.searchBox = 0

    def searchFunc(self):
        if self.var1.get():
            # print(type(self.searchENTRY.get()))
            # PatientFirstName
            newlist = sort.fuzzySearch("PatientFirstName", self.searchENTRY.get(), "str")
            self.updateQueue(newlist)
        elif self.var2.get():
            # First Name
            newlist = sort.fuzzySearch("PatientLastName", self.searchENTRY.get(), "str")
            self.updateQueue(newlist)

        elif self.var3.get():
            # Last Name
            newlist = sort.fuzzySearch("PatientDateOfBirth", self.searchENTRY.get(), "date")
            self.updateQueue(newlist)

        elif self.var4.get():
            # MRN
            newlist = sort.fuzzySearch("PatientMRN", self.searchENTRY, "int")
            self.updateQueue(newlist)
    def resetQueueToDefault(self):
        pass

    def togAdvancedSearch(self):
        if self.advancedSearch == 0:
            self.togFilter()
            self.advancedsearchBUTTON.destroy()
            self.advancedSearchFRAME.destroy()
            self.searchforBUTTON.destroy()
            self.defaultQueueBUTTON.destroy()
            self.advancedsearchBUTTON = Button(self.root, text = "Less\nOptions", command=lambda: self.togAdvancedSearch())
            self.advancedsearchBUTTON.place(x=20, y = 555, width = 75, height = 32.5)
            self.searchforBUTTON = Button(self.root, text = "Advanced\nSearch",bg="blue",fg="white")
            self.searchforBUTTON.place(x=122.5, y = 555, width = 75, height = 32.5)
            self.defaultQueueBUTTON = Button(self.root, text = "Default Work Queue", command=lambda: self.resetQueueToDefault())
            self.defaultQueueBUTTON.place(x=20, y = 525, width = 177.5, height = 25)

            self.var6 = IntVar()
            self.OVERDUESearch = Checkbutton(self.root, text="Days Overdue", variable=self.var6)
            self.OVERDUESearch.place(x=2.5,y=285)

            OVERDUESearchOptions=("Exact Search", "Ascending", "Descending")

            self.OVERDUECombo=Combobox(self.root, values=OVERDUESearchOptions)
            self.OVERDUECombo.place(x=110, y=285, width = 100)


            self.var7 = IntVar()
            self.ageSearch = Checkbutton(self.root, text="Age", variable=self.var7)
            self.ageSearch.place(x=2.5,y=310)

            ageSearchOptions=("Exact Search", "Ascending", "Descending")

            self.ageCombo=Combobox(self.root, values=ageSearchOptions)
            self.ageCombo.place(x=110, y=310, width = 100)


            self.var8 = IntVar()
            self.sexSearch = Checkbutton(self.root, text="Sex", variable=self.var8)
            self.sexSearch.place(x=2.5,y=335)

            sexSearchOptions=("Male", "Female")

            self.sexCombo=Combobox(self.root, values=sexSearchOptions)
            self.sexCombo.place(x=110, y=335, width = 100)


            self.var9 = IntVar()
            self.languageSearch = Checkbutton(self.root, text="Language", variable=self.var9)
            self.languageSearch.place(x=2.5,y=360)

            languageSearchOptions=("English", "Spanish", "French")

            self.languageCombo=Combobox(self.root, values=languageSearchOptions)
            self.languageCombo.place(x=110, y=360, width = 100)

            self.var10 = IntVar()
            self.lastVisitSearch = Checkbutton(self.root, text="Last Visit", variable=self.var10)
            self.lastVisitSearch.place(x=2.5,y=385)

            lastVisitSearchOptions=("Exact Search", "Ascending", "Descending")

            self.lastVisitCombo=Combobox(self.root, values=lastVisitSearchOptions)
            self.lastVisitCombo.place(x=110, y=385, width = 100)



            self.advancedSearch = 1
        else:
            self.advancedsearchBUTTON.destroy()
            self.advancedSearchFRAME.destroy()
            self.searchforBUTTON.destroy()
            self.ageSearch.destroy()
            self.ageCombo.destroy()
            self.sexSearch.destroy()
            self.sexCombo.destroy()
            self.languageCombo.destroy()
            self.languageSearch.destroy()
            self.lastVisitCombo.destroy()
            self.lastVisitSearch.destroy()
            self.OVERDUESearch.destroy()
            self.OVERDUECombo.destroy()
            self.defaultQueueBUTTON.destroy()
            self.searchforBUTTON = Button(self.root, text = "Search",bg="blue",fg="white")
            self.searchforBUTTON.place(x=122.5, y = 320, width = 75, height = 32.5)
            self.advancedsearchBUTTON = Button(self.root, text = "More\nOptions", command=lambda: self.togAdvancedSearch())
            self.advancedsearchBUTTON.place(x=20, y = 320, width = 75, height = 32.5)
            self.defaultQueueBUTTON = Button(self.root, text = "Default Work Queue", command=lambda: self.resetQueueToDefault())
            self.defaultQueueBUTTON.place(x=20, y = 290, width = 177.5, height = 25)
            self.advancedSearchFRAME = LabelFrame(self.root)
            self.advancedSearchFRAME.place(x=0,y=370,height=230,width=225)
            self.togFilter()
            self.advancedSearch = 0

    def togFilter(self):
        if self.filter == 0:

            self.filterLABEL = Label(self.root, text = "Queue Filters")
            self.filterLABEL.place(x=5, y = 375)
            #print("Test")

            filterOptions=("Ascending", "Descending")

            self.filterVar1 = IntVar()
            self.fNameFilter = Checkbutton(self.root, text="First Name", variable=self.filterVar1)
            self.fNameFilter.place(x=2.5,y=400)

            self.fNameFilterCombo=Combobox(self.root, values=filterOptions)
            self.fNameFilterCombo.place(x=110, y=400, width = 100)

            self.filterVar2 = IntVar()
            self.lNameFilter = Checkbutton(self.root, text="Last Name", variable=self.filterVar2)
            self.lNameFilter.place(x=2.5,y=425)

            self.lNameFilterCombo=Combobox(self.root, values=filterOptions)
            self.lNameFilterCombo.place(x=110, y=425, width = 100)

            self.filterVar3 = IntVar()
            self.OverdueFilter = Checkbutton(self.root, text="Days Overdue", variable=self.filterVar3)
            self.OverdueFilter.place(x=2.5,y=450)

            self.OverdueFilterCombo=Combobox(self.root, values=filterOptions)
            self.OverdueFilterCombo.place(x=110, y=450, width = 100)

            SexfiterOptions=("Male", "Female")

            self.filterVar4 = IntVar()
            self.SexFilter = Checkbutton(self.root, text="Sex", variable=self.filterVar4)
            self.SexFilter.place(x=2.5,y=475)

            self.SexFilterCombo=Combobox(self.root, values=SexfiterOptions)
            self.SexFilterCombo.place(x=110, y=475, width = 100)

            ImmunizationfilterOptions=("Vaccine 1", "Vaccine 2", "Vaccine 3", "Vaccine 4")
            self.filterVar5 = IntVar()
            self.ImmunizationFilter = Checkbutton(self.root, text="Immunization", variable=self.filterVar5)
            self.ImmunizationFilter.place(x=2.5,y=500)

            self.ImmunizationFilterCombo=Combobox(self.root, values=ImmunizationfilterOptions)
            self.ImmunizationFilterCombo.place(x=110, y=500, width = 100)

            self.filterVar6 = IntVar()
            self.AgeFilter = Checkbutton(self.root, text="Age", variable=self.filterVar6)
            self.AgeFilter.place(x=2.5,y=525)

            self.AgeFilterCombo=Combobox(self.root, values=filterOptions)
            self.AgeFilterCombo.place(x=110, y=525, width = 100)

            self.filterBUTTON = Button(self.root, text = "Filter",bg="blue",fg="white", command=lambda: self.filterQueue())
            self.filterBUTTON.place(x=122.5, y = 555, width = 75, height = 32.5)

            self.defaultFilterBUTTON = Button(self.root, text = "Default")
            self.defaultFilterBUTTON.place(x=20, y = 555, width = 75, height = 32.5)

            self.filter = 1
        else:
            self.fNameFilter.destroy()
            self.fNameFilterCombo.destroy()
            self.lNameFilter.destroy()
            self.lNameFilterCombo.destroy()
            self.OverdueFilter.destroy()
            self.OverdueFilterCombo.destroy()
            self.SexFilter.destroy()
            self.SexFilterCombo.destroy()
            self.ImmunizationFilter.destroy()
            self.ImmunizationFilterCombo.destroy()
            self.AgeFilter.destroy()
            self.AgeFilterCombo.destroy()
            self.filterBUTTON.destroy()
            self.defaultFilterBUTTON.destroy()
            self.filterLABEL.destroy()

            self.filter = 0



    def determineFilter(self,filter): # determines if filter is Ascending or descending

        if filter.get() == "Ascending":

            return True

        return False

    def filterQueue(self):
        if self.filterVar1.get():
            #First Name
            if self.determineFilter(self.fNameFilterCombo):
                newlist = sort.sortPatients(self.queue, 1, False)
                self.updateQueue(newlist)
            else:
                newlist = sort.sortPatients(self.queue, 1, True)
                self.updateQueue(newlist)

        elif self.filterVar2.get():
            #Last Name
            if self.determineFilter(self.lNameFilterCombo):
                newlist = sort.sortPatients(self.queue, 2, False)
                self.updateQueue(newlist)
            else:
                newlist = sort.sortPatients(self.queue, 2, True)
                self.updateQueue(newlist)

        elif self.filterVar3.get():
            #Days Overdue
            if self.determineFilter(self.OverdueFilterCombo):
                newlist = sort.sortPatients(self.queue, 4, False)
                self.updateQueue(newlist)
            else:
                newlist = sort.sortPatients(self.queue, 4, True)
                self.updateQueue(newlist)

        elif self.filterVar4.get():
            #Sex
             if self.determineFilter(self.SexFilterCombo):
                newlist = sort.sortPatients(self.queue, 6, False)
                self.updateQueue(newlist)
             else:
                newlist = sort.sortPatients(self.queue, 6, True)
                self.updateQueue(newlist)
        elif self.filterVar5.get():
            #Immunization Filter
             if self.determineFilter(self.ImmunizationFilterCombo):
                newlist = sort.sortPatients(self.queue, 7, False)
                self.updateQueue(newlist)
             else:
                newlist = sort.sortPatients(self.queue, 7, True)
                self.updateQueue(newlist)
        elif self.filterVar6.get():
            #Age
            if self.determineFilter(self.AgeFilterCombo):
                newlist = sort.sortPatients(self.queue, 8, False)
                self.updateQueue(newlist)
            else:
                newlist = sort.sortPatients(self.queue, 8, True)
                self.updateQueue(newlist)


        print()


    def setUpQueue(self):
        self.myframe = None
        self.canvas = None
        self.myscrollbar = None
        self.frame = None
        self.scrollHeadFRAME = None
        self.headLABEL = None

    def setUpSearchFrame(self):

        #Search Box
        self.searchBox = 0

        #setup for search box
        self.searchFRAME = None
        self.searchTXT = None
        self.searchENTRY = None
        self.closeSearch = None
        self.FnameSearch = None
        self.fNameCombo = None
        self.LnameSearch = None
        self.LnameCombo = None
        self.DOBSearch = None
        self.DOBCombo = None
        self.MRNSearch = None
        self.MRNCombo = None
        self.OVERDUESearch = None
        self.OVERDUECombo = None
        self.ImmunTypeSearch = None
        self.ImmunTypeCombo = None
        self.searchforBUTTON = None
        self.advancedsearchBUTTON = None
        self.advancedSearchFRAME = None
        self.currentPatient = None

        
    def myfunction(self,event):
        if self.largeQueue == 1:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=350,height=475)
        else:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=575,height=475)
        
    
    def togFileTab(self):
        if self.file == 0:
            self.closeALLTabs()
            #self.fileFRAME = LabelFrame(self.root)
            #self.fileFRAME.place(x=0,y=30,height=120,width=100)
            currentY = 30
            self.mainMenuBUTTON = Button(self.root, text = "Home", justify = LEFT,anchor=W, command=lambda: self.showMainMenu())
            self.mainMenuBUTTON.place(x=0,y=currentY,height=30,width=100)
            currentY = currentY + 30

            if not self.user.permissions == None:
                if self.user.permissions.importData == 1:
                    self.importData = Button(self.root, text = "Import", justify = LEFT,anchor=W)
                    self.importData.place(x=0,y=currentY,height=30,width=100)
                    currentY = currentY + 30

                if self.user.permissions.exportData == 1:
                    self.export = Button(self.root, text = "Export", justify = LEFT,anchor=W, command=lambda: self.togExportTab())
                    self.export.place(x=0,y=currentY,height=30,width=100)
                    currentY = currentY + 30


                if self.user.permissions.printFiles == 1:
                    self.print = Button(self.root, text = "Print", justify = LEFT,anchor=W)
                    self.print.place(x=0,y=currentY,height=30,width=100)
                    currentY = currentY + 30
            
            self.logout = Button(self.root, text = "Log out", justify = LEFT,anchor=W, command=lambda: self.logoutofApp())
            self.logout.place(x=0,y=currentY,height=30,width=100)
            
            self.file = 1
        else:
            #self.fileFRAME.destroy()
            self.mainMenuBUTTON.destroy()
            self.logout.destroy()
            if not self.user.permissions == None:
                if self.user.permissions.exportData == 1:
                    if self.exportTAB == 1:
                        self.togExportTab()
                    self.export.destroy()
                if self.user.permissions.printFiles == 1:
                    self.print.destroy()
                if self.user.permissions.importData == 1:
                    self.importData.destroy()
            self.file = 0

    def togExportTab(self):
        if self.exportTAB == 0:

            self.pdf = Button(self.root, text = ".PDF", justify = LEFT,anchor=W)
            self.pdf.place(x=100,y=30,height=30,width=50)

            self.txt = Button(self.root, text = ".TXT", justify = LEFT,anchor=W)
            self.txt.place(x=100,y=60,height=30,width=50)

            self.cvs = Button(self.root, text = ".CVS", justify = LEFT,anchor=W)
            self.cvs.place(x=100,y=90,height=30,width=50)
            
            self.exportTAB = 1
        else:
            self.pdf.destroy()
            self.txt.destroy()
            self.cvs.destroy()
            self.exportTAB = 0

    def togOptionsTab(self):
        if self.option == 0:
            self.closeALLTabs()

            if self.notificationsTABState == 0:
                self.toggleNotifications = Button(self.root, text = "Hide Notifications", justify = LEFT,anchor=W, command=lambda: self.togNotifications())
                self.toggleNotifications.place(x=50,y=30,height=30,width=110)
            else:
                self.toggleNotifications = Button(self.root, text = "Show Notifications", justify = LEFT,anchor=W, command=lambda: self.togNotifications())
                self.toggleNotifications.place(x=50,y=30,height=30,width=110)
            self.option = 1
        else:
            self.option = 0
            self.toggleNotifications.destroy()

    def togNotifications(self):
        self.closeALLTabs()
        if self.notificationsTABState == 0:
            for n in self.notificationList:
                n.destroy()
            self.notificationList = []
            self.notificationsTABState = 1
        else:
            self.setUpNotifications([[3,"Very Important Message!"],[2,"Important Message."],[1,"Notification Message"]])
            self.notificationsTABState = 0

    def togReportTab(self):
        if self.report == 0:
            self.closeALLTabs()
            self.report = 1
        else:
            self.report = 0

    def togHelpTab(self):
        if self.help == 0:
            self.closeALLTabs()
            self.helpFRAME = LabelFrame(self.root)
            self.helpFRAME.place(x=150,y=30,height=60,width=110)

            self.guide= Button(self.root, text = "Guide", justify = LEFT,anchor=W)
            self.guide.place(x=150,y=30,height=30,width=110)
            
            self.aboutUs= Button(self.root, text = "About US", justify = LEFT,anchor=W)
            self.aboutUs.place(x=150,y=60,height=30,width=110)
            
            self.help = 1
        else:
            self.helpFRAME.destroy()
            self.guide.destroy()
            self.aboutUs.destroy()
            
            self.help = 0

    def togAnalyticsTab(self):
        if self.analytics == 0:
            self.closeALLTabs()
            #self.analyticsFRAME = LabelFrame(self.root)
            #self.analyticsFRAME.place(x=200,y=30,height=200,width=100)

            currentY = 30
            if not self.user.permissions == None:
                if self.user.permissions.viewSelfAnalytics == 1:
                    self.myAnalytics = Button(self.root, text = "My Analytics", justify = LEFT,anchor=W)
                    self.myAnalytics.place(x=self.analyticTABX,y=currentY,height=30,width=110)
                    currentY = currentY + 30

                if self.user.permissions.viewSystemAnalytics == 1:
                    self.systemAnalytics = Button(self.root, text = "System Analytics", justify = LEFT,anchor=W)
                    self.systemAnalytics.place(x=self.analyticTABX,y=currentY,height=30,width=110)
                    currentY = currentY + 30
            
            self.analytics = 1
        else:
            #self.analyticsFRAME.destroy()
            if not self.user.permissions == None:
                if self.user.permissions.viewSelfAnalytics == 1:
                    self.myAnalytics.destroy()
                if self.user.permissions.viewSystemAnalytics == 1:
                    self.systemAnalytics.destroy()
            self.analytics = 0

    def togHistoryTab(self):
        if self.history == 0:
            self.closeALLTabs()

            currentY = 30
            if not self.user.permissions == None:
                if self.user.permissions.viewHistoryOfSelf == 1:
                    self.myHistory = Button(self.root, text = "My History", justify = LEFT,anchor=W)
                    self.myHistory.place(x=self.historyTABX,y=currentY,height=30,width=100)
                    currentY = currentY + 30

                if self.user.permissions.viewHistoryOfEntireSystem == 1:
                    self.systemHistory = Button(self.root, text = "System History", justify = LEFT,anchor=W)
                    self.systemHistory.place(x=self.historyTABX,y=currentY,height=30,width=100)
                    currentY = currentY + 30

            self.history = 1
        else:
            if not self.user.permissions == None:
                if self.user.permissions.viewHistoryOfSelf == 1:
                    self.myHistory.destroy()
                if self.user.permissions.viewHistoryOfEntireSystem == 1:
                    self.systemHistory.destroy()
            self.history = 0

    def togAdminTab(self):
        if self.admin == 0:
            self.closeALLTabs()

            currentY = 30

            if not self.user.permissions == None:
                if self.user.permissions.createAlerts == 1:
                    self.createAlerts = Button(self.root, text = "Alert Manger", justify = LEFT,anchor=W, command=lambda: self.showAlertsSCREEN())
                    self.createAlerts.place(x=self.adminTABX,y=currentY,height=30,width=125)
                    currentY = currentY + 30

                if self.user.permissions.approveUsers == 1:
                    self.accountManager = Button(self.root, text = "Account Manager", justify = LEFT,anchor=W)
                    self.accountManager.place(x=self.adminTABX,y=currentY,height=30,width=125)
                    currentY = currentY + 30

                if self.user.permissions.setPermissions == 1:
                    self.permissions = Button(self.root, text = "Permission Manager", justify = LEFT,anchor=W, command=lambda: self.showPermissionsSCREEN())
                    self.permissions.place(x=self.adminTABX,y=currentY,height=30,width=125)
                    currentY = currentY + 30

                #print(self.user.permissions.setSystemOptions)
                if self.user.permissions.setSystemOptions == 1:
                    self.systemOptions = Button(self.root, text = "System Manager", justify = LEFT, anchor=W)
                    self.systemOptions.place(x=self.adminTABX,y=currentY,height=30,width=125)
                    currentY = currentY + 30

                #print(self.user.permissions.consoleCommands)
                if self.user.permissions.consoleCommands == 1:
                    self.systemConsole = Button(self.root, text = "Console", justify = LEFT, anchor=W, command=lambda: self.showConsole())
                    self.systemConsole.place(x=self.adminTABX,y=currentY,height=30,width=125)
                    currentY = currentY + 30

            self.admin = 1
        else:
            if not self.user.permissions == None:
                if self.user.permissions.createAlerts == 1:
                    self.createAlerts.destroy()
                if self.user.permissions.approveUsers == 1:
                    self.accountManager.destroy()
                if self.user.permissions.setSystemOptions == 1:
                    self.systemOptions.destroy()
                if self.user.permissions.setPermissions == 1:
                    self.permissions.destroy()
                if self.user.permissions.consoleCommands == 1:
                    self.systemConsole.destroy()
            self.admin = 0

    def showPermissionsSCREEN(self):
        self.clearAllScreens()

        self.permissionLabelFRAME = Label(self.root, text = '{0:<15} {1:<35}'.format("Role", "Description"), font = ('Consolas', 10),justify=LEFT, anchor=W)
        self.permissionLabelFRAME.place(x=0, y=102.5, height = 20, width = 400)
            
        self.Permissionmyframe=Frame(self.root,relief=GROOVE,width=20,height=475,bd=1)
        self.Permissionmyframe.place(x=0,y=125,height=475,width=400)

        self.Permissioncanvas=Canvas(self.Permissionmyframe)
        self.Permissionframe=Frame(self.Permissioncanvas)
        self.PermissionmyscrollbarY=Scrollbar(self.Permissionmyframe,orient="vertical",command=self.Permissioncanvas.yview)
        self.Permissioncanvas.configure(yscrollcommand=self.PermissionmyscrollbarY.set)
        self.PermissionmyscrollbarY.pack(side="right",fill="y")

        self.Permissioncanvas.pack(side="left")
        self.Permissioncanvas.create_window((0,0),window=self.Permissionframe,anchor='nw')
        self.Permissionframe.bind("<Configure>", self.Permissionmyfunction)

        self.permissionEditFrame = LabelFrame(self.root)
        self.permissionEditFrame.place(x=400, y = 100, height = 500, width = 400)

        self.permissionEditMainLabel = Label(self.root, text = "Create Role", font = (25))
        self.permissionEditMainLabel.place(x=402.5, y=110, width = 395)

        self.permissionEditNameField = Entry(self.root)
        self.permissionEditNameField.place(x=450, y=150)

        self.permissionEditNameFieldLabel = Label(self.root, text = "Role: ")
        self.permissionEditNameFieldLabel.place(x=410, y=150)

        self.permissionEditDescriptionFieldLabel = Label(self.root, text = "Description:")
        self.permissionEditDescriptionFieldLabel.place(x=410, y=190)

        self.permissionEditDescriptionField = Entry(self.root)
        self.permissionEditDescriptionField.place(x=485, y=190, width = 250)
        

        self.permissionvar1 = IntVar()
        self.permissionImportData = Checkbutton(self.root, text="Import Data", variable=self.permissionvar1)
        self.permissionImportData.place(x=410,y=215)

        self.permissionvar2 = IntVar()
        self.permissionExportData = Checkbutton(self.root, text="Export Data", variable=self.permissionvar2)
        self.permissionExportData.place(x=410,y=240)

        self.permissionvar3 = IntVar()
        self.permissionPersonalHistoryData = Checkbutton(self.root, text="Personal History", variable=self.permissionvar3)
        self.permissionPersonalHistoryData.place(x=410,y=265)

        self.permissionvar4 = IntVar()
        self.permissionSystemHistoryData = Checkbutton(self.root, text="Entire System History", variable=self.permissionvar4)
        self.permissionSystemHistoryData.place(x=410,y=290)

        self.permissionvar5 = IntVar()
        self.permissionPersonalAnalyticsData = Checkbutton(self.root, text="Personal Analytics", variable=self.permissionvar5)
        self.permissionPersonalAnalyticsData.place(x=410,y=315)

        self.permissionvar6 = IntVar()
        self.permissionSystemAnalyticsData = Checkbutton(self.root, text="Entire System Analytics", variable=self.permissionvar6)
        self.permissionSystemAnalyticsData.place(x=410,y=340)

        self.permissionvar7 = IntVar()
        self.permissionCreateAlertsData = Checkbutton(self.root, text="Create Alerts", variable=self.permissionvar7)
        self.permissionCreateAlertsData.place(x=410,y=365)

        self.permissionvar8 = IntVar()
        self.permissionSetPermissionsData = Checkbutton(self.root, text="Set Permissions", variable=self.permissionvar8)
        self.permissionSetPermissionsData.place(x=410,y=390)

        self.permissionvar9 = IntVar()
        self.permissionSearchDatabaseData = Checkbutton(self.root, text="Search in Patient Database", variable=self.permissionvar9)
        self.permissionSearchDatabaseData.place(x=410,y=415)

        self.permissionvar10 = IntVar()
        self.permissionPrintData = Checkbutton(self.root, text="Print Files", variable=self.permissionvar10)
        self.permissionPrintData.place(x=410,y=440)

        self.permissionvar11 = IntVar()
        self.permissionOutreachData = Checkbutton(self.root, text="Out Reach to Patients", variable=self.permissionvar11)
        self.permissionOutreachData.place(x=410,y=465)

        self.permissionvar12 = IntVar()
        self.permissionApproveUsers = Checkbutton(self.root, text="Approve Users", variable=self.permissionvar12)
        self.permissionApproveUsers.place(x=410,y=490)

        self.permissionvar13 = IntVar()
        self.permissionSystemSettings = Checkbutton(self.root, text="Editing of System Settings", variable=self.permissionvar13)
        self.permissionSystemSettings.place(x=410,y=515)

        self.permissionvar14 = IntVar()
        self.permissionConsoleCommands = Checkbutton(self.root, text="Console Commands", variable=self.permissionvar14)
        self.permissionConsoleCommands.place(x=410,y=540)


        self.permissionsPatientsOpenText = Label(self.root, text = "Max Open Patients: ")
        self.permissionsPatientsOpenText.place(x=600,y=215)
        
        self.permissionsPatientsOpen = Entry(self.root)
        self.permissionsPatientsOpen.place(x=715,y=215, width = 30)

        self.permissionsGoalNumberOfOutreachesText = Label(self.root, text = "Goal Outreaches: ")
        self.permissionsGoalNumberOfOutreachesText.place(x=600,y=240)
        
        self.permissionsGoalNumberOfOutreaches = Entry(self.root)
        self.permissionsGoalNumberOfOutreaches.place(x=715,y=240, width = 30)
        
        self.changePermissionBUTTON = Button(self.root, text = "Create New\nRole", bg="blue",fg="white", command=lambda: self.changePermission())
        self.changePermissionBUTTON.place(x=715, y=545, width = 70, height = 40)

        self.deleteRoleButton = None
        
        self.permissionButtonList = []
        self.permssionList = []

        self.addPermissions(self.Permissionframe, self.getPermissions())

        self.permissionsSCREEN = 1

    def getPermissions(self):
        output = self.SQL.getAllPermissions()
        if output == -1:
            return []
        return output

    def getPermission(self):
        return Permissions([self.permissionEditNameField.get(),
                          self.permissionEditDescriptionField.get(),
                          self.permissionvar1.get(),
                          self.permissionvar2.get(),
                          self.permissionvar3.get(),
                          self.permissionvar4.get(),
                          self.permissionvar5.get(),
                          self.permissionvar6.get(),
                          self.permissionvar7.get(),
                          self.permissionvar8.get(),
                          self.permissionvar9.get(),
                          self.permissionvar10.get(),
                          self.permissionvar11.get(),
                          self.permissionvar12.get(),
                          self.permissionvar13.get(),
                          self.permissionvar14.get(),
                          int(self.permissionsPatientsOpen.get()),
                          int(self.permissionsGoalNumberOfOutreaches.get())])

    def clearPermissionEditor(self):
        self.permissionEditNameField.delete(0, END)
        self.permissionEditDescriptionField.delete(0, END)
        
        self.permissionvar1.set(0)
        self.permissionvar2.set(0)
        self.permissionvar3.set(0)
        self.permissionvar4.set(0)
        self.permissionvar5.set(0)
        self.permissionvar6.set(0)
        self.permissionvar7.set(0)
        self.permissionvar8.set(0)
        self.permissionvar9.set(0)
        self.permissionvar10.set(0)
        self.permissionvar11.set(0)
        self.permissionvar12.set(0)
        self.permissionvar13.set(0)
        self.permissionvar14.set(0)
        
        self.permissionsPatientsOpen.delete(0, END)
        self.permissionsGoalNumberOfOutreaches.delete(0, END)
        
    
    def changePermission(self):
        p = self.getPermission()
        if self.currentEditingPermission == None:
            self.createNewPermission(p)
            self.permssionList.append(p)
            self.updatePermissionList(self.permssionList)
        else:
            self.editPermission(self.currentEditingPermission, p)
            for b in self.permissionButtonList:
                b.configure(background = self.root.cget('bg'))
            self.currentButton = None
            self.currentEditingPermission = None
            self.updatePermissionList(self.getPermissions())
        #p = Permission()
        self.clearPermissionEditor()
        for b in self.permissionButtonList:
            b.destroy()

        self.permissionButtonList = []
        self.permssionList = []

        self.addPermissions(self.Permissionframe, self.getPermissions())

        self.currentEditingPermission = None
        self.changePermissionBUTTON.configure(text="Create New\nRole")
        self.permissionEditMainLabel.configure(text="Create Role")
        self.deleteRoleButton.destroy()
        self.deleteRoleButton = None
           
        
        

    def editPermission(self, oldPermission, newPermission):
        self.SQL.editPermission(oldPermission, newPermission)
        

    def deletePermission(self, role):
        self.SQL.deletePermission(role)

        for b in self.permissionButtonList:
            b.destroy()

        self.clearPermissionEditor()
        
        self.permissionButtonList = []
        self.permssionList = []

        self.addPermissions(self.Permissionframe, self.getPermissions())

        self.currentEditingPermission = None
        self.changePermissionBUTTON.configure(text="Create New\nRole")
        self.permissionEditMainLabel.configure(text="Create Role")
        if not self.deleteRoleButton == None:
            self.deleteRoleButton.destroy()
            self.deleteRoleButton = None

    def createNewPermission(self, p):
        self.SQL.addPermission(p)

    def loadPermission(self, permission):
        self.clearPermissionEditor()
        
        self.permissionEditNameField.insert(0,permission.name)
        self.permissionEditDescriptionField.insert(0,permission.description)
        
        self.permissionvar1.set(permission.importData)
        self.permissionvar2.set(permission.exportData)
        self.permissionvar3.set(permission.viewHistoryOfSelf)
        self.permissionvar4.set(permission.viewHistoryOfEntireSystem)
        self.permissionvar5.set(permission.viewSelfAnalytics)
        self.permissionvar6.set(permission.viewSystemAnalytics)
        self.permissionvar7.set(permission.createAlerts)
        self.permissionvar8.set(permission.setPermissions)
        self.permissionvar9.set(permission.serachEntireDatabase)
        self.permissionvar10.set(permission.printFiles)
        self.permissionvar11.set(permission.outReach)
        self.permissionvar12.set(permission.approveUsers)
        self.permissionvar13.set(permission.setSystemOptions)
        self.permissionvar14.set(permission.consoleCommands)
        
        self.permissionsPatientsOpen.insert(0,str(int(permission.numberOfPatientsOpen)))
        #print(type(permission.goalNumberOfOutReaches))
        if not math.isnan(permission.goalNumberOfOutReaches):
            self.permissionsGoalNumberOfOutreaches.insert(0,str(int(permission.goalNumberOfOutReaches)))

    def addPermissions(self, frame, permissionList):
        self.currentEditingPermission = None
        if permissionList == None:
            return
        for i in range(len(permissionList)):
            pstr = '{0:<15} {1:<35}'.format(permissionList[i].name, permissionList[i].description)
            b = Button(frame, text = pstr,anchor=W, justify=LEFT, width = 55, font = ('Consolas', 10))
            b.grid(row=i)
            self.permissionButtonList.append(b)
            self.permssionList.append(permissionList[i])
            b.configure(command=lambda i=i: self.showPermissionEditor(self.permissionButtonList[i], self.permssionList[i]))
            #if self.permssionList[i] == self.currentEditingPermission:
            #    self.currentButton = b
            #   b.configure(background = "lime green")

    def showPermissionEditor(self, button, permission):
        self.clearPermissionEditor()
        if permission == self.currentEditingPermission:
            for b in self.permissionButtonList:
                b.configure(background = self.root.cget('bg'))
            self.currentEditingPermission = None
            self.changePermissionBUTTON.configure(text="Create New\nRole")
            self.permissionEditMainLabel.configure(text="Create Role")
            if not self.deleteRoleButton == None:
                self.deleteRoleButton.destroy()
                self.deleteRoleButton = None
        else:
            for b in self.permissionButtonList:
                b.configure(background = self.root.cget('bg'))
                
            for b in self.permissionButtonList:
                if b == button:
                    b.configure(background = "lime green")
            self.currentEditingPermission = permission
            self.loadPermission(self.currentEditingPermission)
            self.changePermissionBUTTON.configure(text="Change\nRole")
            self.permissionEditMainLabel.configure(text="Edit Role")

            self.deleteRoleButton = Button(self.root, text = "Delete\nRole", bg="blue",fg="white", command=lambda: self.deletePermission(self.permissionEditNameField.get()))
            self.deleteRoleButton.place(x=715, y=495, width = 70, height = 40)


        

    def updatePermissionList(self,newPermissionList):
        for b in self.permissionButtonList:
            b.destroy()
        self.addPermissions(self.Permissionframe, newPermissionList)
        self.queue = newPermissionList
        self.permissionList = None
            
    def closeALLTabs(self):
        if self.file == 1:
            self.togFileTab()

        if self.option == 1:
            self.togOptionsTab()

        if self.report == 1:
            self.togReportTab()

        if self.help == 1:
            self.togHelpTab()

        if self.admin == 1:
            self.togAdminTab()

        if self.analytics == 1:
            self.togAnalyticsTab()

        if self.history ==1:
            self.togHistoryTab()

    def createQueue(self):
        plist = self.SQL.getDefaultWorkQueue()

        if plist == -1:
            return []
        return plist

    def updateQueue(self,newPatientList):
        for b in self.bList:
            b.destroy()
        self.addToQueue(self.frame, newPatientList)
        self.permssionList = newPatientList


    def addToQueue(self, frame, patientList):
        self.bList = []
        for i in range(len(patientList)):
            if self.largeQueue == 1:
                pstr = '{0:<10} {1:<13} {2:<13} {3:<10}'.format(patientList[i].fName, patientList[i].lName, patientList[i].dueDate, patientList[i].daysOverDue)
            
                #FONT has to be monospaced or it wont work
            
                b = Button(frame, text = pstr,anchor=W, justify=LEFT, width = 46, font = ('Consolas', 10))
                b.grid(row=i)
                self.bList.append(b)
                b.configure(command=lambda i=i: self.showPatient(patientList[i].MRN, self.bList[i]))
                if patientList[i].MRN == self.currentPatient:
                     self.currentButton = b
                     b.configure(background = "lime green")
            else:
                pstr = '{0:<15} {1:<13} {2:<13} {3:<10}'.format(patientList[i].fName, patientList[i].lName, patientList[i].dueDate, patientList[i].daysOverDue)
            
                #FONT has to be monospaced or it wont work
            
                b = Button(frame, text = pstr,anchor=W, justify=LEFT, width = 100, font = ('Consolas', 10), command=lambda i=i: self.showPatient(patientList[i].MRN, self.bList[i]))
                b.grid(row=i)
                self.bList.append(b)
                if patientList[i].MRN == self.currentPatient:
                     self.currentButton = b
                     b.configure(background = "lime green")

    def resetWorkQueue(self, mrn):
        for p in self.queue:
            if p.MRN == mrn:
                self.queue.remove(p)
                break
        for b in self.bList:
            b.destroy()

        self.addToQueue(self.frame, self.queue)

    def showPatient(self, MRN, b):
        #hash map would be better
        if self.currentPatient == MRN:
            for button in self.bList:
                button.configure(background = self.root.cget('bg'))
            self.clearPatient()
            self.currentPatient = None
            self.currentButton = None
        else:
            for patient in self.queue:
                if patient.MRN == MRN:
                    self.showSummary(patient)
                    break
            for button in self.bList:
                button.configure(background = self.root.cget('bg'))

            for button in self.bList:
                #print(b == button)
                if b == button:
                    b.configure(background = "lime green")
                    self.currentButton = button
                    break
            self.currentPatient = MRN


        if self.outreach == 1:
            self.reportText.destroy()
            self.outreachText.destroy()
            self.outreachText2.destroy()
            self.callOptions.destroy()
            self.NotesTextArea.destroy()
            self.NotesScrollBar.destroy()
            self.submittOutReach.destroy()
            self.outreach = 0

    def destroyPopOut(self,newWindow):
        newWindow.destroy()
        self.currentPopOut -= 1

    def xPand(self,patient):

        if self.currentPopOut >= self.user.permissions.numberOfPatientsOpen:
            messagebox.showerror("error window", "Too many windows already open!")
            return

        newWindow = Toplevel()
        newWindow.title("Patient Details MRN: " + str(patient.MRN))
        patientInfo = med_INFO_SCREEN(newWindow,patient)
        self.currentPopOut += 1

        #closeButton = Button(newWindow,text="Go Back",command= lambda:self.destroyPopOut(newWindow))
        #closeButton.grid()

        newWindow.wm_protocol('WM_DELETE_WINDOW', lambda newWindow=newWindow: self.destroyPopOut(newWindow))
        #newWindow.protocol("WM_DELETE_WINDOW",self.destroyPopOut(newWindow))

    def showSummary(self, patient):
        self.clearPatient()
        self.summary = 1

        self.infoBUTTON = Button(self.root, text = "Summary", command=lambda: self.showSummary(patient))
        self.infoBUTTON.place(x = 575, y = 100, width = 75, height = 37.5)

        self.medBUTTON = Button(self.root, text = "Medical\nHistory", command=lambda: self.showHistory(patient))
        self.medBUTTON.place(x = 650, y = 100, width = 75, height = 37.5)

        self.contactBUTTON = Button(self.root, text = "Contact", command=lambda: self.showContact(patient))
        self.contactBUTTON.place(x = 725, y = 100, width = 75, height = 37.5)

        patientData = patient.getSummary()
        
        
        self.pFName = Label(self.root, text = "First Name: " +  patientData[0])
        self.pFName.place(x = 590, y = 145)

        self.pLName = Label(self.root, text = "Last Name: " +  patientData[1])
        self.pLName.place(x = 590, y = 175)

        self.pMName = Label(self.root, text = "MI: " +  str(patientData[2]))
        self.pMName.place(x = 730, y = 145)

        self.pDOB = Label(self.root, text = "Date of Birth: " +  patientData[3])
        self.pDOB.place(x = 590, y = 205)

        self.pSex = Label(self.root, text = "Sex: " +  patientData[4])
        self.pSex.place(x = 590, y = 235)

        self.pAge = Label(self.root, text = "Age: " +  patientData[5])
        self.pAge.place(x = 650, y = 235)
        
        self.pRace = Label(self.root, text = "Race: " +  patientData[6])
        self.pRace.place(x = 590, y = 265)

        self.pPrefix = Label(self.root, text = "Prefix: " +  patientData[7])
        self.pPrefix.place(x = 730, y = 175)



        self.expandBUTTON = Button(self.root,text="Expand Patient",command=lambda:self.xPand(patient))
        self.expandBUTTON.place(x=700,y=365, width = 90, height = 30)

        self.outreachBUTTON = Button(self.root,text="Outreach", command=lambda: self.toggleOutReach(patient))
        self.outreachBUTTON.place(x=585,y=365, width = 90, height = 30)

    def showHistory(self, patient):
        self.clearPatient()
        #print(patient)
        historyToShow = self.SQL.getServiceDetails(patient.patientID).values.tolist()
        #print(historyToShow)
        self.phistory = 1

        self.infoBUTTON = Button(self.root, text = "Summary", command=lambda: self.showSummary(patient))
        self.infoBUTTON.place(x = 575, y = 100, width = 75, height = 37.5)

        self.medBUTTON = Button(self.root, text = "Medical\nHistory", command=lambda: self.showHistory(patient))
        self.medBUTTON.place(x = 650, y = 100, width = 75, height = 37.5)

        self.contactBUTTON = Button(self.root, text = "Contact", command=lambda: self.showContact(patient))
        self.contactBUTTON.place(x = 725, y = 100, width = 75, height = 37.5)

        patientData = patient.getHistory()

        self.pHistoryList = []

        self.pmyframe=Frame(self.root,relief=GROOVE,width=50,height=100,bd=1)
        self.pmyframe.place(x=575,y=165,height=170,width=222.5)
        self.pcanvas=Canvas(self.pmyframe)
        self.pframe=Frame(self.pcanvas)
        self.pmyscrollbar=Scrollbar(self.pmyframe, orient="vertical",command=self.pcanvas.yview)
        self.pcanvas.configure(yscrollcommand=self.pmyscrollbar.set)
        self.pmyscrollbar.pack(side="right",fill="y")
        self.pcanvas.pack(side="left")
        self.pcanvas.create_window((0,0),window=self.pframe,anchor='nw')
        self.pframe.bind("<Configure>", self.pmyfunction)

        self.pVaccine(historyToShow)

        headerText = '{0:<15}{1:<8}'.format("Vaccine" , "Date")
        self.pheaderLabel = Label(self.root, text = headerText, font = ("Consolas", 10))
        self.pheaderLabel.place(x = 577.5, y = 140)

        #self.headerLabels = '{0:<10} {1:<13} {2:<8} {3:<10}'.format("First Name", "Last Name", "Due Date", " Days Overdue")
        #self.headLABEL = Label(self.root, anchor= W, justify = LEFT, text = self.headerLabels, font = ("Consolas", 10))
        #self.headLABEL.place(x=227.5, y=102.5,height=20, width = 225)


        '''for history in range(len(patientData[0])):
            newText = '{0:<14}{1:<8}'.format(patientData[0][history][0] , patientData[0][history][1])
            newLabel = Label(self.root, text = newText, font = ("Consolas", 10))
            newLabel.place(x = 580, y = 175 + 30 * history)
            self.pHistoryList.append(newLabel)'''

        '''for history in range(len(patientData[0])):
            newText = patientData[0][history][2]
            newLabel = Label(self.root, text = newText, font = ("Consolas", 10))
            if newText == 'Covered':
                newLabel.config(fg="Green")
            else:
                newLabel.config(fg="Red")
            newLabel.place(x = 720, y = 175 + 30 * history)
            self.pHistoryList.append(newLabel)'''

        #self.pLastVisit = Label(self.root, text = "Last Visit: " + patientData[1], font = ("Consolas", 10))
        #self.pLastVisit.place(x = 580, y = 340)
        
        self.expandBUTTON = Button(self.root,text="Expand Patient",command=lambda:self.xPand(patient))
        self.expandBUTTON.place(x=700,y=365, width = 90, height = 30)

        self.outreachBUTTON = Button(self.root,text="Outreach", command=lambda: self.toggleOutReach(patient))
        self.outreachBUTTON.place(x=585,y=365, width = 90, height = 30)

    def pmyfunction(self,event):
            self.pcanvas.configure(scrollregion=self.pcanvas.bbox("all"),width=222.5,height=170)


    def pVaccine(self, vList):
        self.pVaccineList = []
        for i in range(len(vList)):

            #pstr = '{0:<12} {1:<4}'.format(vList[i][0], vList[i][1])
            #FONT has to be monospaced or it wont work
            #b = Button(self.pframe, text = pstr,anchor=W, justify=LEFT, width = 46, font = ('Consolas', 10))
            #print(vList[i])
            #print(vList[i][7], vList[i][2])
            
            pstr = '{0:<15}{1:<8}'.format(vList[i][7], vList[i][2])
            #FONT has to be monospaced or it wont work
            b = Button(self.pframe, text = pstr,anchor=W, justify=LEFT, width = 46, font = ('Consolas', 10))
            b.grid(row=i)
            self.pVaccineList.append(b)
            #b.configure(command=lambda i=i: self.showPatient(patientList[i].MRN, self.bList[i]))

    def showContact(self, patient):
        self.clearPatient()
        self.contact = 1

        self.infoBUTTON = Button(self.root, text = "Summary", command=lambda: self.showSummary(patient))
        self.infoBUTTON.place(x = 575, y = 100, width = 75, height = 37.5)

        self.medBUTTON = Button(self.root, text = "Medical\nHistory", command=lambda: self.showHistory(patient))
        self.medBUTTON.place(x = 650, y = 100, width = 75, height = 37.5)

        self.contactBUTTON = Button(self.root, text = "Contact", command=lambda: self.showContact(patient))
        self.contactBUTTON.place(x = 725, y = 100, width = 75, height = 37.5)

        patientData = self.SQL.getDemographics(patient.patientID)
        patientData1 = patientData.contact
        patientData2 = patientData.demographics
        
        self.pPhone1 = Label(self.root, text = "Home Phone: " + patientData1[0])
        self.pPhone1.place(x = 580, y = 145)

        self.pPhone2 = Label(self.root, text = "Cell Phone: " + patientData1[1])
        self.pPhone2.place(x = 580, y = 175)

        self.pEmail = Label(self.root, text = "Email: " + patientData1[4])
        self.pEmail.place(x = 580, y = 205)

        self.pLanguage = Label(self.root, text = "Language Preference: " + patientData2[10])
        self.pLanguage.place(x = 580, y = 235)

        self.pContactPreference = Label(self.root, text = "Contact Preference: " + patientData1[5])
        self.pContactPreference.place(x = 580, y = 265)
        
        self.expandBUTTON = Button(self.root,text="Expand Patient",command=lambda:self.xPand(patient))
        self.expandBUTTON.place(x=700,y=365, width = 90, height = 30)

        self.outreachBUTTON = Button(self.root,text="Outreach", command=lambda: self.toggleOutReach(patient))
        self.outreachBUTTON.place(x=585,y=365, width = 90, height = 30)  
        

    def clearPatient(self):
        if self.summary == 1:
            self.outreachBUTTON.destroy()
            self.expandBUTTON.destroy()
            self.infoBUTTON.destroy()
            self.medBUTTON.destroy()
            self.contactBUTTON.destroy()
            
            self.pFName.destroy()
            self.pLName.destroy()
            self.pMName.destroy()
            self.pDOB.destroy()
            self.pAge.destroy()
            self.pRace.destroy()
            self.pSex.destroy()
            self.pPrefix.destroy()
            self.summary = 0
        if self.phistory == 1:
            self.outreachBUTTON.destroy()
            self.expandBUTTON.destroy()
            self.infoBUTTON.destroy()
            self.medBUTTON.destroy()
            self.contactBUTTON.destroy()
            
            for elem in self.pHistoryList:
                elem.destroy()
            self.pheaderLabel.destroy()
            #self.pLastVisit.destroy()
            self.pmyframe.destroy()
            self.pcanvas.destroy()
            self.pframe.destroy()
            self.pmyscrollbar.destroy()
            self.pheaderLabel.destroy()
            for b in self.pVaccineList:
                b.destroy()
            self.phistory = 0
        if self.contact == 1:
            self.outreachBUTTON.destroy()
            self.expandBUTTON.destroy()
            self.infoBUTTON.destroy()
            self.medBUTTON.destroy()
            self.contactBUTTON.destroy()
            self.pPhone1.destroy()
            self.pPhone2.destroy()
            self.pEmail.destroy()
            self.pLanguage.destroy()
            self.pContactPreference.destroy()
            self.contact = 0
            
    def clock(self):
        if self.logout == 0:
            now = datetime.datetime.now()
            current_time = now.strftime("%I:%M %p")
            userInfo = self.userName + " " + str(current_time)
            self.userFRAME.config(text=userInfo)
            self.clockUpdater = self.root.after(1000, self.clock)
            
    def logoutofApp(self):
        self.togFileTab()
        print("Logging out")
        self.user.endSession()
        self.logout = 1
        self.root.after_cancel(self.clockUpdater)
        self.clockUpdater = None
        self.swapTO(Login_Screen.loginScreen, None)
        print("Successful Log out!")

    def togExpandQueue(self):
        self.closeALLTabs()
        if not self.myframe == None:
            self.myframe.destroy()
            self.canvas.destroy()
            self.myscrollbar.destroy()
            self.frame.destroy()
            self.scrollHeadFRAME.destroy()
            self.headLABEL.destroy()
        
        if self.largeQueue == 0:
            self.toggleSearchBox()
            self.togFilter()
            self.myframe=Frame(self.root,relief=GROOVE,width=50,height=100,bd=1)
            self.myframe.place(x=225,y=125,height=475,width=350)

            self.canvas=Canvas(self.myframe)
            self.frame=Frame(self.canvas)
            self.myscrollbar=Scrollbar(self.myframe,orient="vertical",command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.myscrollbar.set)
            self.myscrollbar.pack(side="right",fill="y")
            self.canvas.pack(side="left")
            self.canvas.create_window((0,0),window=self.frame,anchor='nw')
            self.frame.bind("<Configure>", self.myfunction)

            self.scrollHeadFRAME = LabelFrame(self.root, height = 25, width = 350)
            self.scrollHeadFRAME.place(x=225, y=100)

            self.headerLabels = '{0:<10} {1:<13} {2:<8} {3:<10}'.format("First Name", "Last Name", "Due Date", " Days Overdue")
            self.headLABEL = Label(self.root, anchor= W, justify = LEFT, text = self.headerLabels, font = ("Consolas", 10))
            self.headLABEL.place(x=227.5, y=102.5,height=20, width = 345)

            self.largeQueue = 1
            self.addToQueue(self.frame, self.queue)
            

            
        else:
            self.toggleSearchBox()
            if self.filter == 1:
                self.togFilter()
            self.myframe=Frame(self.root,relief=GROOVE,width=50,height=100,bd=1)
            self.myframe.place(x=0,y=125,height=475,width=575)

            self.canvas=Canvas(self.myframe)
            self.frame=Frame(self.canvas)
            self.myscrollbar=Scrollbar(self.myframe,orient="vertical",command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.myscrollbar.set)
            self.myscrollbar.pack(side="right",fill="y")
            self.canvas.pack(side="left")
            self.canvas.create_window((0,0),window=self.frame,anchor='nw')
            self.frame.bind("<Configure>", self.myfunction)

            self.scrollHeadFRAME = LabelFrame(self.root, height = 25, width = 575)
            self.scrollHeadFRAME.place(x=0, y=100)

            self.headerLabels = '{0:<15} {1:<13} {2:<8} {3:<10}'.format("First Name", "Last Name", "Due Date", " Days Overdue")
            self.headLABEL = Label(self.root, anchor= W, justify = LEFT, text = self.headerLabels, font = ("Consolas", 10))
            self.headLABEL.place(x=2.5, y=102.5,height=20, width = 570)

            self.minimizeButton = Button(self.root, command=lambda: self.togExpandQueue())
            self.minimizeButton.place(x= 560, y=102.5, width = 10, height = 10)

            self.largeQueue = 0
            self.addToQueue(self.frame, self.queue)


    def showAlertsSCREEN(self):
        self.clearAllScreens()


        self.alertRoleFRAME = Label(self.root, text = '{0:<15} {1:<35}'.format("Role", "Description"), font = ('Consolas', 10),justify=LEFT, anchor=W)
        self.alertRoleFRAME.place(x=0, y=102.5, height = 20, width = 400)
            
        self.alertRoleMyframe=Frame(self.root,relief=GROOVE,width=20,height=475,bd=1)
        self.alertRoleMyframe.place(x=0,y=125,height=475,width=400)

        self.alertRolecanvas=Canvas(self.alertRoleMyframe)
        self.alertRoleframe=Frame(self.alertRolecanvas)
        self.alertRoleMyscrollbarY=Scrollbar(self.alertRoleMyframe,orient="vertical",command=self.alertRolecanvas.yview)
        self.alertRolecanvas.configure(yscrollcommand=self.alertRoleMyscrollbarY.set)
        self.alertRoleMyscrollbarY.pack(side="right",fill="y")

        self.alertRolecanvas.pack(side="left")
        self.alertRolecanvas.create_window((0,0),window=self.alertRoleframe,anchor='nw')
        self.alertRoleframe.bind("<Configure>", self.alertRoleMyfunction)



        self.alertNotificationMyframe=Frame(self.root,relief=GROOVE,width=20,height=475,bd=1)
        self.alertNotificationMyframe.place(x=400,y=100,height=500,width=400)

        self.alertNotificationcanvas=Canvas(self.alertNotificationMyframe)
        self.alertNotificationframe=Frame(self.alertNotificationcanvas)
        self.alertNotificationMyscrollbarY=Scrollbar(self.alertNotificationMyframe,orient="vertical",command=self.alertNotificationcanvas.yview)
        self.alertNotificationcanvas.configure(yscrollcommand=self.alertNotificationMyscrollbarY.set)
        self.alertNotificationMyscrollbarY.pack(side="right",fill="y")

        self.alertNotificationcanvas.pack(side="left")
        self.alertNotificationcanvas.create_window((0,0),window=self.alertNotificationframe,anchor='nw')
        self.alertNotificationframe.bind("<Configure>", self.alertNotificationMyfunction)


        self.roleButtonList = []
        self.notificationList = []

        self.addAlertRoles(self.alertRoleframe, self.getPermissions())
        

        self.alertSCREEN = 1

        
    def alertRoleMyfunction(self,event):
        self.alertRolecanvas.configure(scrollregion=self.alertRolecanvas.bbox("all"),width=400,height=500)

    def alertNotificationMyfunction(self,event):
        self.alertNotificationcanvas.configure(scrollregion=self.alertNotificationcanvas.bbox("all"),width=400,height=475)

    def addAlertRoles(self, frame, roleList):
        self.currentEditingRoleAlert = None
        if roleList == None:
            return
        for i in range(len(roleList)):
            pstr = '{0:<15} {1:<35}'.format(roleList[i].name, roleList[i].description)
            b = Button(frame, text = pstr,anchor=W, justify=LEFT, width = 55, font = ('Consolas', 10))
            b.grid(row=i)
            self.roleButtonList.append(b)
            self.roleList.append(roleList[i])
            b.configure(command=lambda i=i: self.showNotifcationEditor(self.roleButtonList[i], self.roleList[i]))
            #if self.permssionList[i] == self.currentEditingPermission:
            #    self.currentButton = b
            #   b.configure(background = "lime green")

    def showNotifcationEditor(button, role):
        pass



    def logOut(self,event):
        userChoice = messagebox.askyesno("Logging out", "Are you sure you want\nto log out?")

        if userChoice:
            self.root.after_cancel(self.clockUpdater) # prevents exception error on logout
            self.clockUpdater = None
            self.swapTO(Login_Screen.loginScreen,None)
