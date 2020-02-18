from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk,Image
import datetime
from tkinter import ttk
from Patients import *
from Security import Hash

versionNumber = "(Version 1.7.7b)"

class icaSCREENS():
    '''
    Base class for all screens. Currently will only contain the root,
    clear the screen, and swap to other screens.
    '''
    screenSTACK = []
    def __init__(self,window): #all screens must contain the root window
        self.root = window
        self.root.protocol("WM_DELETE_WINDOW", self.exitICA)

        # insert as "<KEYTYPE>",functionCall.
        self.keyBinds = {}

    def clearSCREEN(self):
        #will clear the screen of everything
        for widget in self.root.winfo_children():
            widget.destroy()

    def swapTO(self,newSCREEN, data): #pass the class of the screen you want to go to along with the window
        self.clearSCREEN()
        newSCREEN(self.root, data)

    def bindKey(self,key,functionCall): # pass a key you want to bind and the function it should call

        self.root.bind(key,functionCall)
        self.keyBinds[key] = functionCall

    def removeKeyBind(self,key): # will remove the bind and free the key for another bind

        self.root.unbind(key)
        del self.keyBinds[key]

    def rebindKey(self,key,functionCall): # will rebind the key to another feature

        self.root.unbind(key)
        self.bindKey(key,functionCall)

    def exitICA(self): #prompt user if they want to close program

        userChoice = messagebox.askyesno("Exiting ICA","Are you sure you want to exit ICA?")

        if userChoice:
            self.root.destroy()

    def escapePress(self,event):
        self.exitICA()

class mainMenu(icaSCREENS):

    def __init__(self,window, user):
        self.user = user
        super().__init__(window)
        #setUpWindow
        global versionNumber
        self.root.geometry("800x600")
        menu = Menu(self.root)
        self.root.title("Immunization Compliance Application " + versionNumber)

        self.bindKey("<Escape>",self.logOut)

        self.clockUpdater = None

        #Max windows open
        self.currentPopOut = 0

        #Set Up  Top Bar
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
        infoDisplayFRAME = LabelFrame(self.root)
        infoDisplayFRAME.place(x=575,y=100,height=500,width=225)
        self.summary = 0
        self.contact = 0
        self.history = 0

        #setupOutReach
        self.reportingFRAME = LabelFrame(self.root)
        self.reportingFRAME.place(x=575,y=400,height=200,width=225)
        self.outreach = 0

        #Notifications based on user in future
        self.setUpNotifications([[3,"Very Important Message!"],[2,"Important Message."],[1,"Notification Message"]])

        #imageSource = "sources/notifications/notification_" + str(1) + ".PNG"
        #notificationImage = Image.open(imageSource)
        #notificationImage = notificationImage.resize((18,18), Image.ANTIALIAS)
        #self.notificationIMAGE = ImageTk.PhotoImage(notificationImage)
        #self.notificationLABEL = Label(self.root,image=self.notificationIMAGE)
        #self.notificationLABEL.place(x=2.5,y= 32.5)

        #update current time
        self.logout = 0
        self.clock()

    def exitICA(self): #prompt user if they want to close program

        userChoice = messagebox.askyesno("Exiting ICA","Are you sure you want to exit ICA?")

        if userChoice:
            self.logoutofApp()
            self.root.destroy()

    def setUpNotifications(self, notifications):
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
                notificationLABEL.place(x=2.5,y= 32.5 + (n * 22.5))
                notificationLABEL1 = Label(self.root, text = notifications[n][1])
                notificationLABEL1.place(x=25,y= 32.5 + (n * 22.5))
            if notifications[n][0] == 2:
                notificationLABEL = Label(self.root,image=self.notificationIMAGE2)
                notificationLABEL.place(x=2.5,y= 32.5 + (n * 22.5))
                notificationLABEL1 = Label(self.root, text = notifications[n][1])
                notificationLABEL1.place(x=25,y= 32.5 + (n * 22.5))
            if notifications[n][0] == 3:
                notificationLABEL = Label(self.root,image=self.notificationIMAGE3)
                notificationLABEL.place(x=2.5,y= 32.5 + (n * 22.5))
                notificationLABEL1 = Label(self.root, text = notifications[n][1])
                notificationLABEL1.place(x=25,y= 32.5 + (n * 22.5))

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

        if self.user.permissions.approveUsers == 1 or self.user.permissions.setPermissions == 1 or self.user.permissions.createAlerts == 1 or self.user.permissions.createAlerts == 1:
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

            self.searchforBUTTON = Button(self.root, text = "Search",bg="blue",fg="white")
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

            self.filterBUTTON = Button(self.root, text = "Filter",bg="blue",fg="white")
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
            self.logout.destroy()
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
            self.option = 1
        else:
            self.option = 0
            
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
            if self.user.permissions.viewSelfAnalytics == 1:
                self.myAnalytics.destroy()
            if self.user.permissions.viewSystemAnalytics == 1:
                self.systemAnalytics.destroy()
            self.analytics = 0

    def togHistoryTab(self):
        if self.history == 0:
            self.closeALLTabs()

            currentY = 30

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
            if self.user.permissions.viewHistoryOfSelf == 1:
                self.myHistory.destroy()
            if self.user.permissions.viewHistoryOfEntireSystem == 1:
                self.systemHistory.destroy()
            self.history = 0

    def togAdminTab(self):
        if self.admin == 0:
            self.closeALLTabs()

            currentY = 30

            if self.user.permissions.createAlerts == 1:
                self.createAlerts = Button(self.root, text = "Alert Manger", justify = LEFT,anchor=W)
                self.createAlerts.place(x=self.adminTABX,y=currentY,height=30,width=125)
                currentY = currentY + 30

            if self.user.permissions.approveUsers == 1:
                self.accountManager = Button(self.root, text = "Account Manager", justify = LEFT,anchor=W)
                self.accountManager.place(x=self.adminTABX,y=currentY,height=30,width=125)
                currentY = currentY + 30

            if self.user.permissions.setPermissions == 1:
                self.permissions = Button(self.root, text = "Permission Manager", justify = LEFT,anchor=W)
                self.permissions.place(x=self.adminTABX,y=currentY,height=30,width=125)
                currentY = currentY + 30

            if self.user.permissions.setSystemOptions == 1:
                self.systemOptions = Button(self.root, text = "System Manager", justify = LEFT, anchor=W)
                self.systemOptions.place(x=self.adminTABX,y=currentY,height=30,width=125)
                currentY = currentY + 30
          
            self.admin = 1
        else:
            if self.user.permissions.createAlerts == 1:
                self.createAlerts.destroy()
            if self.user.permissions.approveUsers == 1:
                self.accountManager.destroy()
            if self.user.permissions.setSystemOptions == 1:
                self.systemOptions.destroy()
            if self.user.permissions.setPermissions == 1:
                self.permissions.destroy()
            
            self.admin = 0

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
        f = open("UITestData.txt", "r")
        pList = []
        for line in f:
            l = line.split()
            pList.append(Patient(l))
        f.close()
        return pList

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
                     b.configure(background = "green")
            else:
                pstr = '{0:<15} {1:<13} {2:<13} {3:<10}'.format(patientList[i].fName, patientList[i].lName, patientList[i].dueDate, patientList[i].daysOverDue)
            
                #FONT has to be monospaced or it wont work
            
                b = Button(frame, text = pstr,anchor=W, justify=LEFT, width = 100, font = ('Consolas', 10), command=lambda i=i: self.showPatient(patientList[i].MRN, self.bList[i]))
                b.grid(row=i)
                self.bList.append(b)
                if patientList[i].MRN == self.currentPatient:
                     self.currentButton = b
                     b.configure(background = "green")

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
                    b.configure(background = "green")
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
        newWindow.title("Patient Details MRN: " + patient.MRN)
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

        self.pMName = Label(self.root, text = "MI: " +  patientData[2])
        self.pMName.place(x = 730, y = 145)

        self.pDOB = Label(self.root, text = "Date of Birth: " +  patientData[3])
        self.pDOB.place(x = 590, y = 205)

        self.pSex = Label(self.root, text = "Sex: " +  patientData[4])
        self.pSex.place(x = 590, y = 235)

        self.pAge = Label(self.root, text = "Age: " +  patientData[5])
        self.pAge.place(x = 650, y = 235)
        
        self.pRace = Label(self.root, text = "Ethnicity: " +  patientData[6])
        self.pRace.place(x = 590, y = 265)

        self.pPrefix = Label(self.root, text = "Prefix: " +  patientData[7])
        self.pPrefix.place(x = 730, y = 175)



        self.expandBUTTON = Button(self.root,text="Expand Patient",command=lambda:self.xPand(patient))
        self.expandBUTTON.place(x=700,y=365, width = 90, height = 30)

        self.outreachBUTTON = Button(self.root,text="Outreach", command=lambda: self.toggleOutReach(patient))
        self.outreachBUTTON.place(x=585,y=365, width = 90, height = 30)

    def showHistory(self, patient):
        self.clearPatient()
        self.history = 1

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

        self.pVaccine(patientData[0])

        headerText = '{0:<10}{1:<8}{2:<10}'.format("Vaccine" , "Overdue", "Insurance")
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

        self.pLastVisit = Label(self.root, text = "Last Visit: " + patientData[1], font = ("Consolas", 10))
        self.pLastVisit.place(x = 580, y = 340)
        
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

            
            pstr = '{0:<12} {1:<4} {2:<10}'.format(vList[i][0], vList[i][1], vList[i][2])
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

        patientData = patient.getContact()
        
        self.pPhone = Label(self.root, text = "Phone: " + patientData[0][0] + "     Type: " + patientData[0][1])
        self.pPhone.place(x = 580, y = 145)

        self.pEmail = Label(self.root, text = "Email: " + patientData[1])
        self.pEmail.place(x = 580, y = 175)

        self.pLanguage = Label(self.root, text = "Language Preference: " + patientData[2])
        self.pLanguage.place(x = 580, y = 205)

        self.pContactPreference = Label(self.root, text = "Contact Preference: " + patientData[3])
        self.pContactPreference.place(x = 580, y = 235)
        
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
        if self.history == 1:
            self.outreachBUTTON.destroy()
            self.expandBUTTON.destroy()
            self.infoBUTTON.destroy()
            self.medBUTTON.destroy()
            self.contactBUTTON.destroy()
            
            for elem in self.pHistoryList:
                elem.destroy()
            self.pheaderLabel.destroy()
            self.pLastVisit.destroy()
            self.pmyframe.destroy()
            self.pcanvas.destroy()
            self.pframe.destroy()
            self.pmyscrollbar.destroy()
            self.pheaderLabel.destroy()
            for b in self.pVaccineList:
                b.destroy()
            self.history = 0
        if self.contact == 1:
            self.outreachBUTTON.destroy()
            self.expandBUTTON.destroy()
            self.infoBUTTON.destroy()
            self.medBUTTON.destroy()
            self.contactBUTTON.destroy()
            
            self.pPhone.destroy()
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
        self.swapTO(loginScreen, None)
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



    def logOut(self,event):
        userChoice = messagebox.askyesno("Logging out", "Are you sure you want\nto log out?")

        if userChoice:
            self.root.after_cancel(self.clockUpdater) # prevents exception error on logout
            self.clockUpdater = None
            self.swapTO(loginScreen,None)

class med_INFO_SCREEN(icaSCREENS):


    def __init__(self, window, Patient):
        super().__init__(window)
        self.root.geometry("800x600")
        self.bindKey("<Escape>",self.closeWindow)

        self.thisPatient = Patient
        self.currentUser = None
        self.insurance = None
        self.demoGraphics = None
        self.immunizationHistory = None


        #setup the notebook for patient screen
        self.patientNotebook = ttk.Notebook(self.root,width=500,height=500)
        self.demosPage = ttk.Frame(self.patientNotebook)


        self.servicePage = ttk.Frame(self.patientNotebook)
        self.contactPage = ttk.Frame(self.patientNotebook)
        self.insurancePage = ttk.Frame(self.patientNotebook)

        self.patientNotebook.add(self.demosPage,text="Demographics")
        self.patientNotebook.add(self.servicePage, text="Service History")
        self.patientNotebook.add(self.contactPage, text="Outreach Report")
        self.patientNotebook.add(self.insurancePage,text="Insurance")

        self.patientNotebook.place(x=100,y=100)

        self.patientFrame = LabelFrame(self.root,width=1000,height=30,bg="Blue")
        self.patientFrame.place(x=0,y=0)

        self.patientFULL = Patient.fName + " " + Patient.lName

        #format; FULL Name, Gender, Age <years> DOB, MRN
        self.patientLabelText = '{0:<27}{1:<17}{2:<10}{3:<17}{4:<10}'.format("PATIENT:" + self.patientFULL,"GENDER: Female","AGE:50 ",
                                                                             "DOB:3/21/2013","MRN:30")

        self.patientLabel = Label(self.patientFrame, text=self.patientLabelText, font=('Consolas', 14),bg="Blue",fg="White")
        self.patientLabel.place(x=0, y=0)


        self.buttonFrame = LabelFrame(self.root, width=100, height=560)
        self.buttonFrame.place(x=0, y=40)


        menuItems = ['Garantour ', 'Last Service', 'Create\n Outreach\n form', 'Immunization\nHistory',]


        for index in range(len(menuItems)):

            menuButton = Button(self.buttonFrame,text=menuItems[index],width=12,height=3)
            menuButton.pack()

        #Contact info
        self.nameLabel = None
        self.language = None
        self.address = None
        self.email = None
        self.phone = None
        self.commentsBox = None
        self.outreachDate = None
        self.methodDropDown = None
        self.outCome = None
        self.apptDate = None



        #ExtensionWindow
        self.extensionFrame = LabelFrame(self.root,width=200,height=500)
        self.extensionFrame.place(x=600,y=100)






        self.showDemos()
        self.showService()
        self.showOutReach()

    def showDemos(self): # uses self.demosPage for display

        patientFrame = LabelFrame(self.demosPage,text="<Patient>",width=500,height=65)
        patientFrame.place(x=0,y=25)
        patientFrame.grid_propagate(False)

        self.label_and_Text(patientFrame,"Lastname",0,0,self.thisPatient.lName)

        self.label_and_Text(patientFrame,"Firstname",0,4,self.thisPatient.fName)

        self.label_and_Text(patientFrame,"Middle Initial",0,8,"Init")

        self.label_and_Text(patientFrame, "Prefix", 0, 12, "Ms.")

        self.label_and_Text(patientFrame, "NickName", 0,16, "nick")

        patientFrame.grid_columnconfigure(4, minsize=100)
        patientFrame.grid_rowconfigure(2,minsize=25)


        demoFrame = LabelFrame(self.demosPage,text="<Demographics>",width=500,height=65)
        demoFrame.place(x=0,y=100)
        demoFrame.grid_propagate(False)


        self.label_and_Text(demoFrame, "Sex", 0, 0, "Female")
        self.label_and_Text(demoFrame, "DOB", 0, 2, "2/20/2013")
        self.label_and_Text(demoFrame, "Pref. Language", 0, 4, "English")
        self.label_and_Text(demoFrame, "Race", 0, 6, "Caucasian")
        self.label_and_Text(demoFrame, "Ethnicity", 0, 8, "White")
        self.label_and_Text(demoFrame, "Age", 0, 10, "50")

        demoFrame.grid_columnconfigure(4, minsize=100)
        demoFrame.grid_rowconfigure(2, minsize=25)

        addressFrame = LabelFrame(self.demosPage,text="<Address>",width=500,height=125)
        addressFrame.place(x=0,y=175)
        addressFrame.grid_propagate(False)

        self.label_and_Text(addressFrame,"Street 1",0,0,"1234 random Street")
        self.label_and_Text(addressFrame, "Street 2", 4, 0, "1234 random Street 2")
        self.label_and_Text(addressFrame, "Zipcode", 0, 2, "00000")
        self.label_and_Text(addressFrame, "City", 0, 3, "Pacific City")
        self.label_and_Text(addressFrame, "State", 4, 2, "CA")
        self.label_and_Text(addressFrame, "County", 4,3, "randomCounty")
        self.label_and_Text(addressFrame, "Country", 0,4, "Some Country")

        addressFrame.grid_columnconfigure(4, minsize=120)
        addressFrame.grid_rowconfigure(2, minsize=25)

        contactFrame = LabelFrame(self.demosPage,text="<Contact>",width=500,height=175)
        contactFrame.place(x=0,y=300)
        contactFrame.grid_propagate(False)

        self.label_and_Text(contactFrame, "Phone", 0, 0, "123-456-789")
        self.label_and_Text(contactFrame, "Mobile", 4, 0, "987-654-321")
        self.label_and_Text(contactFrame, "Work Phone", 0, 2, "123-456-789")
        self.label_and_Text(contactFrame, "Email", 0, 4, "r_Andom@u.pacific.edu")
        self.label_and_Text(contactFrame, "Preferred Contact", 4,2 , "Mobile")

        contactLabel = Label(contactFrame,text= "Contact Notes")
        contactLabel.grid(row=4, column=4)

        self.contactNotes = Text(contactFrame,width=30,height=3,padx=5)
        self.contactNotes.place(x=230,y=100)
        self.contactNotes.insert('end',"Notes about contacting this patient here")
        self.contactNotes.configure(state=DISABLED)


        contactFrame.grid_columnconfigure(4, minsize=100)
        contactFrame.grid_rowconfigure(2, minsize=50)


    def label_and_Text(self,frame,labelText,labelRow,labelCol,boxText):
        '''
        Used to create format for demos page
        '''

        lNameLabel = Label(frame, text='{0:<10}'.format(labelText))
        lNameLabel.grid(row=labelRow, column=labelCol,padx=10)

        patientLname = Text(frame, width=len(boxText), height=1,padx=5)
        patientLname.insert('end', boxText)
        patientLname.configure(state=DISABLED)
        patientLname.grid(row=labelRow+2, column=labelCol)


    def showService(self): # uses servicePage Canvas for display

        #formate Service ID, Immunization Name, Compliance, Service Date, Extra Tab?
        formatString = '{0:<12}{1:<15}{2:<12}{3:<15}{4:<8}'.format("Service ID","Immunization",
                                                             "Compliance","Service Date","Extra")

        formatLabel = Label(self.servicePage, text=formatString, font=('Consolas', 11)
                            , relief="raised",pady=10)
        formatLabel.pack()


    def loadServiceHistory(self):

        pass



    def showOutReach(self): # uses patient Canvas for display

        contactFrame = LabelFrame(self.contactPage, text="<Contact>",width=500,height=120)
        contactFrame.place(x=0, y=25)
        contactFrame.grid_propagate(False)

        self.label_and_Text(contactFrame, "Phone", 0, 0, "123-456-789")
        self.label_and_Text(contactFrame, "Mobile", 4, 0, "987-654-321")
        self.label_and_Text(contactFrame, "Work Phone", 0, 2, "123-456-789")
        self.label_and_Text(contactFrame, "Email", 0, 4, "r_Andom@u.pacific.edu")
        self.label_and_Text(contactFrame, "Preferred Contact", 4, 2, "Mobile")
        self.label_and_Text(contactFrame, "Pref. Language", 4, 4, "English")


        #contact notes and outreach notes
        notesLabel = Label(self.contactPage,text="Contact Notes")
        notesLabel.place(x=75,y=150)

        contactNotes = Text(self.contactPage,width=30,height=4,padx=5)
        contactNotes.place(x=0,y=175)
        contactNotes.insert('end',"Notes about contacting this patient here")

        outreachNotesLabel = Label(self.contactPage, text="Outreach Notes")
        outreachNotesLabel.place(x=350, y=150)

        self.outreachNotes = Text(self.contactPage, width=27, height=4,padx=5)
        self.outreachNotes.place(x=275, y=175)

        contactNotesButton = Button(self.contactPage,text="Submit Changes")
        contactNotesButton.place(x=50,y=250)


        #contact Method Frame
        contactMethodFrame = LabelFrame(self.contactPage, text="<Method of contact>",width=500,height=200)
        contactMethodFrame.place(x=0,y=300)
        contactMethodFrame.grid_propagate(False)

        emailPatient = Button(contactMethodFrame,text="Email Patient",command=self.extensionEmail)
        emailPatient.place(x=25,y=25)



    def getPatientHistory(self):
        pass

    def getPatientDemographics(self):
        pass

    def closeWindow(self,event):

        self.root.destroy()


    def extensionEmail(self): # will display extension for emailing patient
        '''
        Things still need to implemented:
        minimize/saving
        close button
        loading in templates
        '''

        tempLabel = Label(self.extensionFrame,text="Minimize/Exit Button goes here")
        tempLabel.place(x=0,y=0)

        displayLabel = Label(self.extensionFrame,text="To:" + self.patientFULL ,font = ('Consolas', 14),relief="groove")
        displayLabel.place(x=0,y=25)

        templateLabel = Label(self.extensionFrame,text="<Email Template>")
        templateLabel.place(x=0,y=75)

        self.emailText = Text(self.extensionFrame,width=24,height=15)
        self.emailText.place(x=0,y=100)

        buttonFrame = LabelFrame(self.extensionFrame,text="<Email Options>",width=200,height=150)
        buttonFrame.place(x=0,y=350)

        template1 = Button(buttonFrame,text="Load\n Template 1",command=lambda: self.loadTemplate(1))
        template1.place(x=20,y=10)


        template2 = Button(buttonFrame,text="Load\n Template 2",command=lambda: self.loadTemplate(2))
        template2.place(x=100,y=10)

        sendEmail = Button(buttonFrame,text="Send Email!",command=self.sendEmail)
        sendEmail.place(x=20,y=75)

        clearEmail = Button(buttonFrame,text="Clear Email",command=self.clearEmailEntry)
        clearEmail.place(x=100,y=75)

    def loadTemplate(self,version): # will load a email template file into extension before sending

        if self.emailText:
            self.clearEmailEntry()


        Filename = "email_template_" + str(version) +".txt"

        chosenFile = open(Filename)

        text = chosenFile.readlines()
        text[0] = "Dear " + self.patientFULL + ", \n" # insert patient name into email

        fullText = ""

        for line in text:
            fullText += line

        self.emailText.insert('end',fullText)

    def sendEmail(self):
        userChoice = messagebox.askyesno("Sending Email", "Send Email to " + self.patientFULL + "?")

        length = len(self.emailText.get("1.0",END))

        if userChoice and length != 1: # checks if user wants to send email and if email actually has text
            #send email functionality here:

            messagebox.showinfo("Sent!", "Email sent to " + self.patientFULL + "!")

            self.clearEmailEntry() # clear the email screen
            return

        if length == 1:
            messagebox.showinfo("Empty email","Please include the message you would like to send to " + self.patientFULL)
            return


    def clearEmailEntry(self): # clears the email text box
        self.emailText.delete("1.0", END)

    def clearExtension(self): # will clear the extension Frame

        for widget in self.extensionFrame.winfo_children():
            widget.destroy()


#History of action classes

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
        self.userType = data[3]
        if isNewSession == 1:
            self.currentUserSession = UserSession(self.userId, None)

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

class loginScreen(icaSCREENS):

    def __init__(self, window, data):
        super().__init__(window)
        self.root.geometry("800x600")
        global versionNumber
        self.root.title("Immunization Compliance Application " + versionNumber)

        self.background = Canvas(self.root,width=800,height=600)
        self.background.place(x=0,y=0)

        self.bindKey("<Return>",self.enterPress)
        self.bindKey("<Escape>",self.escapePress)

        self.loginBackGround = Canvas(self.root,width=500,height=250)
        self.loginBackGround.place(x=150,y=275)

        image = Image.open("sources/ica picture.PNG")
        image = image.resize((700,200), Image.ANTIALIAS)
        self.titleIMAGE = ImageTk.PhotoImage(image)

        self.imageLABEL = Label(self.root,image=self.titleIMAGE)

        self.imageLABEL.place(x=50,y=25)


        self.userNameLabel = Label(self.root,text="Username: ",font=('Consolas', 16))
        self.userNameLabel.place(x=200,y=300)

        self.userNameEntry = Entry(self.root,width=25,font=(16))
        self.userNameEntry.place(x=350,y=305)

        self.passwordLabel = Label(self.root, text="Password: ", font=('Consolas', 16))
        self.passwordLabel.place(x=200, y=350)

        self.passwordEntry = Entry(self.root, width=25, font=(16),show="*")
        self.passwordEntry.place(x=350, y=355)


        self.loginButton = Button(self.root,text="Login!",bg="light blue",fg="black",width=13,height=2,command=self.verifyUser)
        self.loginButton.place(x=350,y=400)

        self.cancelButton = Button(self.root,text="Cancel",bg="light blue",fg="black",width=13,height=2,command=self.exitICA)
        self.cancelButton.place(x=475,y=400)

        self.userNameLabel = Label(self.root,text=versionNumber[1:-1],font=('Consolas', 16))
        self.userNameLabel.place(x=5,y=575)

    def verifyUser(self):
        name = self.userNameEntry.get()
        passWord = self.passwordEntry.get()

        #Would send Hash.main(name) to data base and recieve hashed pword from database
        #check if Hash.main(passWord) == recieved hashed pword

        tempUserName = "f69ddcc92c44eb5a6320e241183ef551d9287d7fa6e4b2c77459145d8dd0bb37" # Test01

        tempPassWord = "b575f55adf6ed25767832bdf6fe6cbc4af4889938bf48ba99698ec683f9047de" # Test02

        tempUserName1 = "67ed235e1e075a7214902e1af0cb4bb4ad3ba0fcf084411418074cf4247004cc" # User01

        tempPassWord1 = "7bab9c019f082639a163c437288ed2fe6da3e08a447cf9b8487f7c3535613fda" # User02

        if Hash.main(name) == tempUserName and Hash.main(passWord) == tempPassWord: #admin test account

            #querry User here
            currentUser = User([0, "Admin", "", "Admin"], 1)

            messagebox.showinfo("Login Successful!", "Welcome back " + currentUser.userFirstName)#needs to be User first name
            self.removeKeyBind("<Return>")

            self.swapTO(mainMenu, currentUser)#needs to be user object

        elif Hash.main(name) == tempUserName1 and Hash.main(passWord) == tempPassWord1: #user test Account

            #querry User here
            currentUser = User([0, "User", "", "User"], 1)

            messagebox.showinfo("Login Successful!", "Welcome back " + currentUser.userFirstName)#needs to be User first name
            self.removeKeyBind("<Return>")

            self.swapTO(mainMenu, currentUser)#needs to be user object

        else:
            messagebox.showerror("Login Unsuccessful", "Username or Password is invalid")
            self.passwordEntry.delete(0,END) #remove password

    def enterPress(self,event):
        self.verifyUser()

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
        self.userType = data[3]
        if isNewSession == 1:
            self.currentUserSession = UserSession(self.userId, None)
        #Querry User Permissions Here
        if self.userType == "Admin":
            self.permissions = Permissions([1,1,1,1,1,1,1,1,1,1,1,1,10,100,1])
        else:
            self.permissions = Permissions([0,0,1,0,1,0,0,0,1,1,0,0,5,50,0])

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

def main(): # Main loop of ICA
    window = Tk()
    window.resizable(0, 0)
    window.title(versionNumber)

    #currentSCREEN = loginScreen(window, None)

    currentUser = User([0, "Jason", "Van Bladel", "Admin"], 1)
    currentSCREEN = mainMenu(window, currentUser)

    #currentSCREEN = med_INFO_SCREEN(window,Patient(["John","Smith","20","2/3/2013","32","30"]))

    window.mainloop()

main()
