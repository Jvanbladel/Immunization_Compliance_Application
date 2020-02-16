from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk,Image
import datetime
from tkinter import ttk
from Patients import *

versionNumber = "(Version 1.6.2b)"


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
        self.userName = data[0]
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        userInfo = self.userName + " " + str(current_time)
        self.userFRAME = Label(self.root,text=userInfo,anchor=E, justify=RIGHT)
        self.userFRAME.place(x=572.5,y=2.5,height=25,width=225)

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

        #setupOutReach
        self.reportingFRAME = LabelFrame(self.root)
        self.reportingFRAME.place(x=575,y=400,height=200,width=225)
        self.outreach = 0

        #update current time
        self.clock()

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
        print("Out Reach", patient.fName)

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
        self.currentPatient = None

        
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
        if self.currentPatient == MRN:
            for button in self.bList:
                button.configure(background = self.root.cget('bg'))
            self.clearPatient()
            self.currentPatient = None
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
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        userInfo = self.userName + " " + str(current_time)
        self.userFRAME.config(text=userInfo)
        #lab['text'] = time
        self.root.after(1000, self.clock)
            
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

    def getHistory(zelf):
        return [[["Flu", "45", "Covered"], ["Hepatitis B", "12", "Covered"], ["Pollo", "325", "Uncovered"], ["Chickpox", "15", "Uncovered"], ["MMR", "749", "Partial"], ["Rotavirus","45", "Covered"], ["Yellow Fever", "365", "Partial"]], "3/23/14"]

    def getContact(self):
        return [["(925)980-4048", "Mobile"], "austin@gmail.com", "English", "Phone"]

    def getFullSummary(self):
        return None
    
    def getFullHistory(self):
        return None

    def getFullContact(self):
        return None

    def getFullInsurance(self):
        return None

    def getGarentor(self):
        return None

    def getLastService(self):
        return None

    def getFullImmunizationHistory(self):
        return None


class med_INFO_SCREEN(icaSCREENS):


    def __init__(self, window, Patient):
        super().__init__(window)
        self.root.geometry("800x600")

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

        self.showDemos()


        self.showContact()

    def showDemos(self): # uses self.demosPage for display

        patientFrame = LabelFrame(self.demosPage,text="<Patient>")
        patientFrame.place(x=0,y=25)

        self.label_and_Text(patientFrame,"Lastname",0,0,self.thisPatient.lName)

        self.label_and_Text(patientFrame,"Firstname",0,4,self.thisPatient.fName)

        self.label_and_Text(patientFrame,"Middle Initial",0,8,"Init")

        self.label_and_Text(patientFrame, "Prefix", 0, 12, "Ms.")

        self.label_and_Text(patientFrame, "NickName", 0,16, "nick")

        patientFrame.grid_columnconfigure(4, minsize=100)
        patientFrame.grid_rowconfigure(2,minsize=25)


        demoFrame = LabelFrame(self.demosPage,text="<Demographics>")
        demoFrame.place(x=0,y=100)

        self.label_and_Text(demoFrame, "Sex", 0, 0, "Female")
        self.label_and_Text(demoFrame, "DOB", 0, 2, "2/20/2013")
        self.label_and_Text(demoFrame, "Pref. Language", 0, 4, "English")
        self.label_and_Text(demoFrame, "Race", 0, 6, "Caucasian")
        self.label_and_Text(demoFrame, "Ethnicity", 0, 8, "White")
        self.label_and_Text(demoFrame, "Age", 0, 10, "50")

        demoFrame.grid_columnconfigure(4, minsize=100)
        demoFrame.grid_rowconfigure(2, minsize=25)

        addressFrame = LabelFrame(self.demosPage,text="<Address>")
        addressFrame.place(x=0,y=175)

        self.label_and_Text(addressFrame,"Street 1",0,0,"1234 random Street")
        self.label_and_Text(addressFrame, "Street 2", 4, 0, "1234 random Street 2")
        self.label_and_Text(addressFrame, "Zipcode", 0, 2, "00000")
        self.label_and_Text(addressFrame, "City", 0, 3, "Pacific City")
        self.label_and_Text(addressFrame, "State", 4, 2, "CA")
        self.label_and_Text(addressFrame, "County", 4,3, "randomCounty")
        self.label_and_Text(addressFrame, "Country", 0,4, "Some Country")

        addressFrame.grid_columnconfigure(4, minsize=120)
        addressFrame.grid_rowconfigure(2, minsize=25)

        contactFrame = LabelFrame(self.demosPage,text="<Contact>")
        contactFrame.place(x=0,y=300)

        self.label_and_Text(contactFrame, "Phone", 0, 0, "123-456-789")
        self.label_and_Text(contactFrame, "Mobile", 4, 0, "987-654-321")
        self.label_and_Text(contactFrame, "Work Phone", 0, 2, "123-456-789")
        self.label_and_Text(contactFrame, "Email", 0, 4, "r_Andom@u.pacific.edu")
        self.label_and_Text(contactFrame, "Preferred Contact", 4,2 , "Mobile")

        contactLabel = Label(contactFrame,text= "Contact Notes")
        contactLabel.grid(row=4, column=4)



        contactFrame.grid_columnconfigure(4, minsize=100)
        contactFrame.grid_rowconfigure(2, minsize=25)


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


    def showService(self): # uses patient Canvas for display
        pass

    def showContact(self): # uses patient Canvas for display

        #place email/contact info this Frame
        contactFrame = Frame(self.contactPage,width=100,height=100)
        contactFrame.place(x=0,y=0)

        contactEmail = Label(contactFrame,text="Patient Email: ")
        contactEmail.place(x=25,y=25)


    def getPatientHistory(self):
        pass

    def getPatientDemographics(self):
        pass


class loginScreen(icaSCREENS):

    def __init__(self, window, data):
        super().__init__(window)
        self.root.title("ICA")
        self.root.geometry("800x600")
        self.background = Canvas(self.root,width=800,height=600)
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

def main(): # Main loop of ICA
    window = Tk()
    window.resizable(0, 0)
    window.title(versionNumber)

    currentSCREEN = loginScreen(window, None)

    #currentSCREEN = mainMenu(window, ["Jason Van Bladel"])

    #currentSCREEN = med_INFO_SCREEN(window,Patient(["John","Smith","20","2/3/2013","32","30"]))

    window.mainloop()

main()
