from icaScreens import *


class mainMenu(icaSCREENS):

    def __init__(self, window, data):
        super().__init__(window)
        global versionNumber
        self.root.geometry("800x600")
        menu = Menu(self.root)
        self.currentPopOut = 0

        self.root.title("Immunization Compliance Application " + versionNumber)

        myframe = Frame(self.root, relief=GROOVE, width=50, height=100, bd=1)
        myframe.place(x=225, y=125, height=475, width=350)

        self.canvas = Canvas(myframe)
        frame = Frame(self.canvas)
        myscrollbar = Scrollbar(myframe, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0, 0), window=frame, anchor='nw')
        frame.bind("<Configure>", self.myfunction)

        scrollHeadFRAME = LabelFrame(self.root, height=25, width=350)
        scrollHeadFRAME.place(x=225, y=100)

        headerLabels = '{0:<10} {1:<13} {2:<8} {3:<10}'.format("First Name", "Last Name", "Due Date", " Days Overdue")
        headLABEL = Label(self.root, anchor=W, justify=LEFT, text=headerLabels, font=("Consolas", 10))
        headLABEL.place(x=227.5, y=102.5, height=20, width=345)

        searchFRAME = LabelFrame(self.root)
        searchFRAME.place(x=0, y=100, height=500, width=225)

        searchTXT = Label(self.root, text="Search: ")
        searchTXT.place(x=2.5, y=120)

        self.searchENTRY = Entry(self.root)
        self.searchENTRY.place(x=50, y=120, width=160)

        # Options for first Name
        self.var1 = IntVar()
        FnameSearch = Checkbutton(self.root, text="First Name", variable=self.var1)
        FnameSearch.place(x=2.5, y=160)

        fNameSearchOptions = ("Exact Search", "Ascending", "Descending", "Fuzy Search")

        self.fNameCombo = Combobox(self.root, values=fNameSearchOptions)
        self.fNameCombo.place(x=110, y=160, width=100)

        # Options for last Name
        self.var2 = IntVar()
        LnameSearch = Checkbutton(self.root, text="Last Name", variable=self.var2)
        LnameSearch.place(x=2.5, y=185)

        lNameSearchOptions = ("Exact Search", "Ascending", "Descending", "Fuzy Search")

        self.lNameCombo = Combobox(self.root, values=lNameSearchOptions)
        self.lNameCombo.place(x=110, y=185, width=100)

        # Options for Due Date
        self.var3 = IntVar()
        dueDateSearch = Checkbutton(self.root, text="Due Date", variable=self.var3)
        dueDateSearch.place(x=2.5, y=210)

        dueDateSearchOptions = ("Exact Search", "Ascending", "Descending", "Fuzy Search")

        self.fNameCombo = Combobox(self.root, values=dueDateSearchOptions)
        self.fNameCombo.place(x=110, y=210, width=100)

        # Options for days Overdue
        self.var4 = IntVar()
        OVERDUESearch = Checkbutton(self.root, text="Days Overdue", variable=self.var4)
        OVERDUESearch.place(x=2.5, y=235)

        OVERDUESearchOptions = ("Exact Search", "Ascending", "Descending")

        self.OVERDUECombo = Combobox(self.root, values=OVERDUESearchOptions)
        self.OVERDUECombo.place(x=110, y=235, width=100)

        # Options for MRN
        self.var5 = IntVar()
        MRNSearch = Checkbutton(self.root, text="MRN", variable=self.var5)
        MRNSearch.place(x=2.5, y=260)

        MRNSearchOptions = ("Exact Search", "Ascending", "Descending", "Fuzy Search")

        self.MRNCombo = Combobox(self.root, values=MRNSearchOptions)
        self.MRNCombo.place(x=110, y=260, width=100)

        # Options for Immunizations Type
        self.var6 = IntVar()
        ImmunTypeSearch = Checkbutton(self.root, text="Immunization", variable=self.var6)
        ImmunTypeSearch.place(x=2.5, y=285)

        ImmunTypeSearchOptions = ("Vaccine 1", "Vaccine 2", "Vaccine 3", "Vaccine 4")

        self.ImmunTypeCombo = Combobox(self.root, values=ImmunTypeSearchOptions)
        self.ImmunTypeCombo.place(x=110, y=285, width=100)

        # Search Buttons

        searchforBUTTON = Button(self.root, text="Search", bg="blue", fg="white")
        searchforBUTTON.place(x=122.5, y=320, width=75, height=32.5)

        advancedsearchBUTTON = Button(self.root, text="More\nOptions")
        advancedsearchBUTTON.place(x=20, y=320, width=75, height=32.5)

        advancedSearchFRAME = LabelFrame(self.root)
        advancedSearchFRAME.place(x=0, y=370, height=230, width=225)

        infoDisplayFRAME = LabelFrame(self.root)
        infoDisplayFRAME.place(x=575, y=100, height=500, width=225)

        reportingFRAME = LabelFrame(self.root)
        reportingFRAME.place(x=575, y=400, height=500, width=225)

        barFRAME = LabelFrame(self.root)
        barFRAME.place(x=0, y=0, height=30, width=800)

        fileBUTTON = Button(self.root, text="File", command=lambda: self.togFileTab())
        fileBUTTON.place(x=0, y=0, height=30, width=50)

        optionsBUTTON = Button(self.root, text="Options", command=lambda: self.togOptionsTab())
        optionsBUTTON.place(x=50, y=0, height=30, width=50)

        reportBUTTON = Button(self.root, text="Reports", command=lambda: self.togReportTab())
        reportBUTTON.place(x=100, y=0, height=30, width=50)

        helpBUTTON = Button(self.root, text="Help", command=lambda: self.togHelpTab())
        helpBUTTON.place(x=150, y=0, height=30, width=50)

        analyticBUTTON = Button(self.root, text="Analytics", command=lambda: self.togAnalyticsTab())
        analyticBUTTON.place(x=200, y=0, height=30, width=60)

        adminBUTTON = Button(self.root, text="Admin", command=lambda: self.togAdminTab())
        adminBUTTON.place(x=260, y=0, height=30, width=50)

        userName = data[0]
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        userInfo = userName + " " + str(current_time)
        userFRAME = Label(self.root, text=userInfo, anchor=E, justify=RIGHT)
        userFRAME.place(x=572.5, y=2.5, height=25, width=225)

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
        self.export = None
        self.exportFRAME = None
        self.pdf = None
        self.txt = None
        self.cvs = None
        self.pName = None

        # TABS
        self.file = 0
        self.option = 0
        self.report = 0
        self.help = 0
        self.admin = 0
        self.analytics = 0

        # SubTabs
        self.exportTAB = 0

        # patintInfo
        self.summary = 0

        self.queue = []

        self.queue = self.createQueue()

        self.addToQueue(frame, self.queue)

    def myfunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=350, height=475)

    def togFileTab(self):
        if self.file == 0:
            self.closeALLTabs()
            self.fileFRAME = LabelFrame(self.root)
            self.fileFRAME.place(x=0, y=30, height=90, width=100)

            self.export = Button(self.root, text="Export", justify=LEFT, anchor=W, command=lambda: self.togExportTab())
            self.export.place(x=0, y=30, height=30, width=100)

            self.print = Button(self.root, text="Print", justify=LEFT, anchor=W)
            self.print.place(x=0, y=60, height=30, width=100)

            self.logout = Button(self.root, text="Log out", justify=LEFT, anchor=W, command=lambda: self.logoutofApp())
            self.logout.place(x=0, y=90, height=30, width=100)

            self.file = 1
        else:
            if self.exportTAB == 1:
                self.togExportTab()
            self.fileFRAME.destroy()
            self.logout.destroy()
            self.export.destroy()
            self.print.destroy()
            self.file = 0

    def togExportTab(self):
        if self.exportTAB == 0:
            self.exportFRAME = LabelFrame(self.root)
            self.exportFRAME.place(x=100, y=30, height=90, width=50)

            self.pdf = Button(self.root, text=".PDF", justify=LEFT, anchor=W)
            self.pdf.place(x=100, y=30, height=30, width=50)

            self.txt = Button(self.root, text=".TXT", justify=LEFT, anchor=W)
            self.txt.place(x=100, y=60, height=30, width=50)

            self.cvs = Button(self.root, text=".CVS", justify=LEFT, anchor=W)
            self.cvs.place(x=100, y=90, height=30, width=50)

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
            self.optionFRAME.place(x=50, y=30, height=200, width=100)
            self.option = 1
        else:
            self.optionFRAME.destroy()
            self.option = 0

    def togReportTab(self):
        if self.report == 0:
            self.closeALLTabs()
            self.reportFRAME = LabelFrame(self.root)
            self.reportFRAME.place(x=100, y=30, height=200, width=100)
            self.report = 1
        else:
            self.reportFRAME.destroy()
            self.report = 0

    def togHelpTab(self):
        if self.help == 0:
            self.closeALLTabs()
            self.helpFRAME = LabelFrame(self.root)
            self.helpFRAME.place(x=150, y=30, height=60, width=110)

            self.guide = Button(self.root, text="Guide", justify=LEFT, anchor=W)
            self.guide.place(x=150, y=30, height=30, width=110)

            self.aboutUs = Button(self.root, text="About US", justify=LEFT, anchor=W)
            self.aboutUs.place(x=150, y=60, height=30, width=110)

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
            self.analyticsFRAME.place(x=200, y=30, height=200, width=100)

            self.analytics = 1
        else:
            self.analyticsFRAME.destroy()
            self.analytics = 0

    def togAdminTab(self):
        if self.admin == 0:
            self.closeALLTabs()
            self.adminFRAME = LabelFrame(self.root)
            self.adminFRAME.place(x=260, y=30, height=90, width=110)

            self.accountManager = Button(self.root, text="Account Manager", justify=LEFT, anchor=W)
            self.accountManager.place(x=260, y=30, height=30, width=110)

            self.userHistory = Button(self.root, text="User History", justify=LEFT, anchor=W)
            self.userHistory.place(x=260, y=60, height=30, width=110)

            self.permissions = Button(self.root, text="Permissions", justify=LEFT, anchor=W)
            self.permissions.place(x=260, y=90, height=30, width=110)

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
        bList = []
        for i in range(len(patientList)):
            pstr = '{0:<10} {1:<13} {2:<13} {3:<10}'.format(patientList[i].fName, patientList[i].lName,
                                                            patientList[i].dueDate, patientList[i].daysOverDue)

            # FONT has to be monospaced or it wont work
            b = Button(frame, text=pstr, anchor=W, justify=LEFT, width=46, font=('Consolas', 10),
                       command=lambda i=i: self.showPatient(patientList[i].MRN))
            b.grid(row=i)
            bList.append(b)

    def showPatient(self, MRN):
        # hash map would be better
        for patient in self.queue:
            if patient.MRN == MRN:
                self.showSummary(patient)
                break

    def destroyPopOut(self, newWindow):
        newWindow.destroy()
        self.currentPopOut -= 1

    def xPand(self, patient):

        if self.currentPopOut >= 5:
            messagebox.showerror("error window", "Too many windows already open!")
            return

        newWindow = Toplevel()
        newWindow.title("This the patient info")
        patientInfo = med_INFO_SCREEN(newWindow, patient)
        self.currentPopOut += 1

        # closeButton = Button(newWindow,text="Go Back",command= lambda:self.destroyPopOut(newWindow))
        # closeButton.grid()

        newWindow.wm_protocol('WM_DELETE_WINDOW', lambda newWindow=newWindow: self.destroyPopOut(newWindow))
        # newWindow.protocol("WM_DELETE_WINDOW",self.destroyPopOut(newWindow))

    def showSummary(self, patient):
        self.clearPatient()
        self.summary = 1

        info = Button(self.root, text="Summary")
        info.place(x=575, y=100, width=75, height=37.5)

        med = Button(self.root, text="Medical\nHistory")
        med.place(x=650, y=100, width=75, height=37.5)

        med = Button(self.root, text="Contact")
        med.place(x=725, y=100, width=75, height=37.5)

        # self.summaryText = Label(self.root, text = "Patient Information:", font = (12))
        # self.summaryText.place(x = 577.5, y = 102.5)

        self.pName = Label(self.root, text="First Name: " + patient.fName)
        self.pName.place(x=600, y=145)

        expand = Button(self.root, text="Expand Patient", command=lambda: self.xPand(patient))
        expand.place(x=700, y=365, width=90, height=30)

        outreach = Button(self.root, text="Outreach")
        outreach.place(x=585, y=365, width=90, height=30)

    def clearPatient(self):
        if self.summary == 1:
            self.pName.destroy()

    def logoutofApp(self):
        self.togFileTab()
        print("Logging out")
        self.swapTO(loginScreen, None)
        print("Successful Log out!")