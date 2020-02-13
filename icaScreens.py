from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk,Image
import datetime

versionNumber = "Alpha 1.1"

class icaSCREENS():
    '''
    Base class for all screens. Currently will only contain the root,
    clear the screen, and swap to other screens.
    '''
    screenSTACK = []
    def __init__(self,window): #all screens must contain the root window
        self.root = window
        self.root.protocol("WM_DELETE_WINDOW", self.exitICA)


    def clearSCREEN(self):
        #will clear the screen of everything
        for widget in self.root.winfo_children():
            widget.destroy()

    def swapTO(self,newSCREEN, data): #pass the class of the screen you want to go to along with the window
        self.clearSCREEN()
        newSCREEN(self.root, data)

    def exitICA(self): #prompt user if they want to close program
        userChoice = messagebox.askyesno("Exiting ICA","Are you sure you want to exit ICA?")

        if userChoice:
            self.root.destroy()

class mainMenu(icaSCREENS):

    def __init__(self,window, data):
        super().__init__(window)
        #setUpWindow
        global versionNumber
        self.root.geometry("800x600")
        menu = Menu(self.root)
        self.root.title("Immunization Compliance Application " + versionNumber)

        #Max windows open
        self.currentPopOut = 0

        #Set Up  Top Bar
        barFRAME = LabelFrame(self.root)
        barFRAME.place(x=0,y=0,height=30,width=800)

        #Add Name/date to top bar
        userName = data[0]
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        userInfo = userName + " " + str(current_time)
        userFRAME = Label(self.root,text=userInfo,anchor=E, justify=RIGHT)
        userFRAME.place(x=572.5,y=2.5,height=25,width=225)

        #Add tabs to top bar
        self.setUpTabs()
        
        #set Up Search Frame
        self.setUpSearchFrame()

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

        #setUpContact Frame
        reportingFRAME = LabelFrame(self.root)
        reportingFRAME.place(x=575,y=400,height=200,width=225)

        contactOptions=("Answered", "Missed Call", "Hung Up", "Will Call Back", "No Number on File", "Wrong Number", "Attempt Again Later")
        self.callOptions=Combobox(self.root, values=contactOptions)
        self.callOptions.place(x=590,y=420)

        self.submittOutReach = Button(self.root, text = "Submit",command=lambda: self.submitOutReachAttempt())
        self.submittOutReach.place(x= 700, y=450)

    def submitOutReachAttempt(self):
        print("Out Reach")

    def setUpTabs(self):
        fileBUTTON = Button(self.root,text="File",command=lambda: self.togFileTab())
        fileBUTTON.place(x=0,y=0,height=30,width=50)

        optionsBUTTON = Button(self.root,text="Options",command=lambda: self.togOptionsTab())
        optionsBUTTON.place(x=50,y=0,height=30,width=50)

        reportBUTTON = Button(self.root,text="Reports",command=lambda: self.togReportTab())
        reportBUTTON.place(x=100,y=0,height=30,width=50)

        helpBUTTON = Button(self.root,text="Help",command=lambda: self.togHelpTab())
        helpBUTTON.place(x=150,y=0,height=30,width=50)

        analyticBUTTON = Button(self.root,text="Analytics",command=lambda: self.togAnalyticsTab())
        analyticBUTTON.place(x=200,y=0,height=30,width=60)

        adminBUTTON = Button(self.root,text="Admin",command=lambda: self.togAdminTab())
        adminBUTTON.place(x=260,y=0,height=30,width=50)

        #Set Up for TABS
        self.fileFRAME = None
        self.optionFRAME = None
        self.reportFRAME = None
        self.helpFRAME = None
        self.adminFRAME = None
        self.analyticsFRAME = None
        self.logout = None
        self.permissions = None
        self.userHistory = None
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

        #SubTabs
        self.exportTAB = 0
        

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

            #Options for days Overdue
            self.var5 = IntVar()
            self.OVERDUESearch = Checkbutton(self.root, text="Days Overdue", variable=self.var5)
            self.OVERDUESearch.place(x=2.5,y=260)

            OVERDUESearchOptions=("Exact Search", "Ascending", "Descending")
            
            self.OVERDUECombo=Combobox(self.root, values=OVERDUESearchOptions)
            self.OVERDUECombo.place(x=110, y=260, width = 100)

            #Options for Immunizations Type
            self.var6 = IntVar()
            self.ImmunTypeSearch = Checkbutton(self.root, text="Immunization", variable=self.var6)
            self.ImmunTypeSearch.place(x=2.5,y=285)

            ImmunTypeSearchOptions=("Vaccine 1", "Vaccine 2", "Vaccine 3", "Vaccine 4")
            
            self.ImmunTypeCombo=Combobox(self.root, values=ImmunTypeSearchOptions)
            self.ImmunTypeCombo.place(x=110, y=285, width = 100)

            #Search Buttons

            self.searchforBUTTON = Button(self.root, text = "Search",bg="blue",fg="white")
            self.searchforBUTTON.place(x=122.5, y = 320, width = 75, height = 32.5)

            self.advancedsearchBUTTON = Button(self.root, text = "More\nOptions")
            self.advancedsearchBUTTON.place(x=20, y = 320, width = 75, height = 32.5)


            self.advancedSearchFRAME = LabelFrame(self.root)
            self.advancedSearchFRAME.place(x=0,y=370,height=230,width=225)
        
            self.searchBox = 1
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
            self.OVERDUESearch.destroy()
            self.OVERDUECombo.destroy()
            self.ImmunTypeSearch.destroy()
            self.ImmunTypeCombo.destroy()
            self.searchforBUTTON.destroy()
            self.advancedsearchBUTTON.destroy()
            self.advancedSearchFRAME.destroy()
            self.searchBox = 0

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

        
    def myfunction(self,event):
        if self.largeQueue == 1:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=350,height=475)
        else:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=575,height=475)
        
    
    def togFileTab(self):
        if self.file == 0:
            self.closeALLTabs()
            self.fileFRAME = LabelFrame(self.root)
            self.fileFRAME.place(x=0,y=30,height=120,width=100)

            self.importData = Button(self.root, text = "Import", justify = LEFT,anchor=W)
            self.importData.place(x=0,y=30,height=30,width=100)
            
            self.export = Button(self.root, text = "Export", justify = LEFT,anchor=W, command=lambda: self.togExportTab())
            self.export.place(x=0,y=60,height=30,width=100)

            self.print = Button(self.root, text = "Print", justify = LEFT,anchor=W)
            self.print.place(x=0,y=90,height=30,width=100)
            
            self.logout = Button(self.root, text = "Log out", justify = LEFT,anchor=W, command=lambda: self.logoutofApp())
            self.logout.place(x=0,y=120,height=30,width=100)
            
            self.file = 1
        else:
            if self.exportTAB == 1:
                self.togExportTab()
            self.fileFRAME.destroy()
            self.logout.destroy()
            self.export.destroy()
            self.print.destroy()
            self.importData.destroy()
            self.file = 0

    def togExportTab(self):
        if self.exportTAB == 0:
            self.exportFRAME = LabelFrame(self.root)
            self.exportFRAME.place(x=100,y=30,height=90,width=50)

            self.pdf = Button(self.root, text = ".PDF", justify = LEFT,anchor=W)
            self.pdf.place(x=100,y=30,height=30,width=50)

            self.txt = Button(self.root, text = ".TXT", justify = LEFT,anchor=W)
            self.txt.place(x=100,y=60,height=30,width=50)

            self.cvs = Button(self.root, text = ".CVS", justify = LEFT,anchor=W)
            self.cvs.place(x=100,y=90,height=30,width=50)
            
            self.exportTAB = 1
        else:
            self.exportFRAME.destroy()
            self.pdf.destroy()
            self.txt.destroy()
            self.cvs.destroy()
            self.exportTAB = 0

    def togOptionsTab(self):
        if self.option == 0:
            self.closeALLTabs()
            self.optionFRAME = LabelFrame(self.root)
            self.optionFRAME.place(x=50,y=30,height=200,width=100)
            self.option = 1
        else:
            self.optionFRAME.destroy()
            self.option = 0
            
    def togReportTab(self):
        if self.report == 0:
            self.closeALLTabs()
            self.reportFRAME = LabelFrame(self.root)
            self.reportFRAME.place(x=100,y=30,height=200,width=100)
            self.report = 1
        else:
            self.reportFRAME.destroy()
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
            self.analyticsFRAME = LabelFrame(self.root)
            self.analyticsFRAME.place(x=200,y=30,height=200,width=100)
            
            self.analytics = 1
        else:
            self.analyticsFRAME.destroy()
            self.analytics = 0

    def togAdminTab(self):
        if self.admin == 0:
            self.closeALLTabs()
            self.adminFRAME = LabelFrame(self.root)
            self.adminFRAME.place(x=260,y=30,height=90,width=110)

            self.accountManager = Button(self.root, text = "Account Manager", justify = LEFT,anchor=W)
            self.accountManager.place(x=260,y=30,height=30,width=110)

            self.userHistory = Button(self.root, text = "User History", justify = LEFT, anchor=W)
            self.userHistory.place(x=260,y=60,height=30,width=110)

            self.permissions = Button(self.root, text = "Permissions", justify = LEFT,anchor=W)
            self.permissions.place(x=260,y=90,height=30,width=110)
          
            self.admin = 1
        else:
            self.adminFRAME.destroy()
            self.accountManager.destroy()
            self.userHistory.destroy()
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
            if self.largeQueue == 0:
                pstr = '{0:<10} {1:<13} {2:<13} {3:<10}'.format(patientList[i].fName, patientList[i].lName, patientList[i].dueDate, patientList[i].daysOverDue)
            
                #FONT has to be monospaced or it wont work
            
                b = Button(frame, text = pstr,anchor=W, justify=LEFT, width = 46, font = ('Consolas', 10))
                b.grid(row=i)
                self.bList.append(b)
                b.configure(command=lambda i=i: self.showPatient(patientList[i].MRN, self.bList[i]))
            else:
                pstr = '{0:<15} {1:<13} {2:<13} {3:<10}'.format(patientList[i].fName, patientList[i].lName, patientList[i].dueDate, patientList[i].daysOverDue)
            
                #FONT has to be monospaced or it wont work
            
                b = Button(frame, text = pstr,anchor=W, justify=LEFT, width = 100, font = ('Consolas', 10), command=lambda i=i: self.showPatient(patientList[i].MRN, b))
                b.grid(row=i)
                self.bList.append(b)
            

    def showPatient(self, MRN, b):
        #hash map would be better
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
                break

    def destroyPopOut(self,newWindow):
        newWindow.destroy()
        self.currentPopOut -= 1

    def xPand(self,patient):

        if self.currentPopOut >= 5:
            messagebox.showerror("error window", "Too many windows already open!")
            return

        newWindow = Toplevel()
        newWindow.title("This the patient info")
        patientInfo = med_INFO_SCREEN(newWindow,patient)
        self.currentPopOut += 1

        #closeButton = Button(newWindow,text="Go Back",command= lambda:self.destroyPopOut(newWindow))
        #closeButton.grid()

        newWindow.wm_protocol('WM_DELETE_WINDOW', lambda newWindow=newWindow: self.destroyPopOut(newWindow))
        #newWindow.protocol("WM_DELETE_WINDOW",self.destroyPopOut(newWindow))

    def showSummary(self, patient):
        self.clearPatient()
        self.summary = 1

        info = Button(self.root, text = "Summary", command=lambda: self.showSummary(patient))
        info.place(x = 575, y = 100, width = 75, height = 37.5)

        med = Button(self.root, text = "Medical\nHistory", command=lambda: self.showHistory(patient))
        med.place(x = 650, y = 100, width = 75, height = 37.5)

        med = Button(self.root, text = "Contact", command=lambda: self.showContact(patient))
        med.place(x = 725, y = 100, width = 75, height = 37.5)

        self.pInfo = Label(self.root, text = "First Name: " + patient.fName)
        self.pInfo.place(x = 600, y = 145)

        expand = Button(self.root,text="Expand Patient",command=lambda:self.xPand(patient))
        expand.place(x=700,y=365, width = 90, height = 30)

        outreach = Button(self.root,text="Outreach")
        outreach.place(x=585,y=365, width = 90, height = 30)

    def showHistory(self, patient):
        self.clearPatient()
        self.history = 1

        info = Button(self.root, text = "Summary", command=lambda: self.showSummary(patient))
        info.place(x = 575, y = 100, width = 75, height = 37.5)

        med = Button(self.root, text = "Medical\nHistory", command=lambda: self.showHistory(patient))
        med.place(x = 650, y = 100, width = 75, height = 37.5)

        med = Button(self.root, text = "Contact", command=lambda: self.showContact(patient))
        med.place(x = 725, y = 100, width = 75, height = 37.5)

        self.pInfo = Label(self.root, text = "History: ")
        self.pInfo.place(x = 600, y = 145)

        expand = Button(self.root,text="Expand Patient",command=lambda:self.xPand(patient))
        expand.place(x=700,y=365, width = 90, height = 30)

        outreach = Button(self.root,text="Outreach")
        outreach.place(x=585,y=365, width = 90, height = 30)

    def showContact(self, patient):
        self.clearPatient()
        self.history = 1

        info = Button(self.root, text = "Summary", command=lambda: self.showSummary(patient))
        info.place(x = 575, y = 100, width = 75, height = 37.5)

        med = Button(self.root, text = "Medical\nHistory", command=lambda: self.showHistory(patient))
        med.place(x = 650, y = 100, width = 75, height = 37.5)

        med = Button(self.root, text = "Contact", command=lambda: self.showContact(patient))
        med.place(x = 725, y = 100, width = 75, height = 37.5)

        self.pInfo = Label(self.root, text = "Contact: ")
        self.pInfo.place(x = 600, y = 145)

        expand = Button(self.root,text="Expand Patient",command=lambda:self.xPand(patient))
        expand.place(x=700,y=365, width = 90, height = 30)

        outreach = Button(self.root,text="Outreach")
        outreach.place(x=585,y=365, width = 90, height = 30)  
        

    def clearPatient(self):
        if self.summary == 1:
            self.pInfo.destroy()
            
    def logoutofApp(self):
        self.togFileTab()
        print("Logging out")
        self.swapTO(loginScreen, None)
        print("Successful Log out!")

    def togExpandQueue(self):

        if not self.myframe == None:
            self.myframe.destroy()
            self.canvas.destroy()
            self.myscrollbar.destroy()
            self.frame.destroy()
            self.scrollHeadFRAME.destroy()
            self.headLABEL.destroy()
        
        if self.largeQueue == 0:
            self.toggleSearchBox()
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

            self.addToQueue(self.frame, self.queue)
            
            self.largeQueue = 1
            
        else:
            self.toggleSearchBox()
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

            self.addToQueue(self.frame, self.queue)
            
            self.largeQueue = 0
       

class Patient():
    def __init__(self, data):
        self.fName = data[0]
        self.lName = data[1]
        self.score = data[2]
        self.dueDate = data[3]
        self.MRN = data[4]
        self.daysOverDue = data[5]

    def getHistory():
        return None

    def getContact():
        return None
           

class med_INFO_SCREEN(icaSCREENS):
    '''
    Currently very basic. will have more features soon
    '''
    def __init__(self,window,Patient):
        super().__init__(window)
        self.dataBoxes = []

        titles = ["First Name", "Last Name", "Score", "Due Date", "Days over Due", "MRN"]
        defaultEntry = [Patient.fName,Patient.lName,Patient.score,Patient.dueDate,Patient.daysOverDue,Patient.MRN]

        for index in range(6):
            newLABEL = Label(self.root, text=titles[index])
            newLABEL.grid(row=index, column=0)

            newENTRY = Entry(self.root, width=30)
            newENTRY.grid(row=index, column=1)
            newENTRY.insert(0, defaultEntry[index])
            self.dataBoxes.append(newENTRY)

        submitData = Button(self.root, text="Submit Changes", command=self.submitDATA)
        submitData.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

    def submitDATA(self):
            data = []

            for entry in self.dataBoxes:
                # need some way to check for no changes/errors
                thisDATA = entry.get()

                if not thisDATA:  # need an index checking
                    messagebox.showinfo("missing data", "Missing an entry...")
                    return

                data.append(thisDATA)

                #entry.delete(0, END)  # clear entry box

            # send to database here
            messagebox.showinfo("Data Sent!", "Data successfully sent to the database!")

class loginScreen(icaSCREENS):

    def __init__(self, window, data):
        super().__init__(window)
        self.root.title("ICA")
        self.root.geometry("800x600")
        self.background = Canvas(self.root,width=800,height=600,bg="light blue")
        self.background.place(x=0,y=0)


        self.loginBackGround = Canvas(self.root,width=500,height=250)
        self.loginBackGround.place(x=150,y=275)


        self.userName = "Test01"
        self.passWord = "Test02"

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

    def verifyUser(self):
        name = self.userNameEntry.get()
        passWord = self.passwordEntry.get()

        #Would hash and verify user with database here
        if name == self.userName and passWord == self.passWord:
            messagebox.showinfo("Login Successful!", "Welcome back " + str(name))
            self.swapTO(mainMenu, [self.userName])
        else:
            messagebox.showerror("Login Unsuccessful", "Username or Password is invalid")
            self.passwordEntry.delete(0,END) #remove password



def main():
    window = Tk()
    window.resizable(0,0)
    #currentSCREEN = loginScreen(window, None)

    currentSCREEN = mainMenu(window, ["Jason Van Bladel"])
    window.mainloop()


main()
