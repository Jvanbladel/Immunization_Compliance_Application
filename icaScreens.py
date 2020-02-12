from tkinter import *
from tkinter import messagebox
import sqlite3
import datetime

class icaSCREENS():
    '''
    Base class for all screens. Currently will only contain the root,
    clear the screen, and swap to other screens.
    '''
    screenSTACK = []
    def __init__(self,window): #all screens must contain the root window
        self.root = window

    def clearSCREEN(self):
        #will clear the screen of everything
        for widget in self.root.winfo_children():
            widget.destroy()

    def swapTO(self,newSCREEN, data): #pass the class of the screen you want to go to along with the window
        self.clearSCREEN()
        newSCREEN(self.root, data)

class mainMenu(icaSCREENS):

    def __init__(self,window, data):
        super().__init__(window)

        self.root.geometry("800x600")
        menu = Menu(self.root)
        self.currentPopOut = 0


        myframe=Frame(self.root,relief=GROOVE,width=50,height=100,bd=1)
        myframe.place(x=225,y=100,height=500,width=350)

        self.canvas=Canvas(myframe)
        frame=Frame(self.canvas)
        myscrollbar=Scrollbar(myframe,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=frame,anchor='nw')
        frame.bind("<Configure>", self.myfunction)

        searchFRAME = LabelFrame(self.root)
        searchFRAME.place(x=0,y=100,height=500,width=225)
    
        
        searchTXT = Label(self.root, text = "Search: ")
        searchTXT.place(x=2.5,y=120)
        
        self.searchENTRY = Entry(self.root)
        self.searchENTRY.place(x=50,y=120,width=150)

        var1 = IntVar()
        LnameSearch = Checkbutton(self.root, text="Last Name", variable=var1)
        LnameSearch.place(x=2.5,y=160)

        var2 = IntVar()
        FnameSearch = Checkbutton(self.root, text="First Name", variable=var2)
        FnameSearch.place(x=100,y=160)

        var3 = IntVar()
        MRNSearch = Checkbutton(self.root, text="MRN", variable=var3)
        MRNSearch.place(x=2.5,y=190)

        var4 = IntVar()
        DueDateSearch = Checkbutton(self.root, text="Due Date", variable=var4)
        DueDateSearch.place(x=100,y=190)
        

        infoDisplayFRAME = LabelFrame(self.root)
        infoDisplayFRAME.place(x=575,y=100,height=500,width=225)

        reportingFRAME = LabelFrame(self.root)
        reportingFRAME.place(x=575,y=400,height=500,width=225)

        barFRAME = LabelFrame(self.root)
        barFRAME.place(x=0,y=0,height=30,width=800)

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

        userName = data[0]
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        userInfo = userName + " " + str(current_time)
        userFRAME = Label(self.root,text=userInfo,anchor=E, justify=RIGHT)
        userFRAME.place(x=572.5,y=2.5,height=25,width=225)

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
        
        #TABS
        self.file = 0
        self.option = 0
        self.report = 0
        self.help = 0
        self.admin = 0
        self.analytics = 0

        #SubTabs
        self.exportTAB = 0

        #patintInfo
        self.summary = 0

        self.queue = []

        self.queue = self.createQueue()
        
        self.addToQueue(frame, self.queue)
        
    def myfunction(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=350,height=500)
    
    def togFileTab(self):
        if self.file == 0:
            self.closeALLTabs()
            self.fileFRAME = LabelFrame(self.root)
            self.fileFRAME.place(x=0,y=30,height=90,width=100)
            
            self.export = Button(self.root, text = "Export", justify = LEFT,anchor=W, command=lambda: self.togExportTab())
            self.export.place(x=0,y=30,height=30,width=100)

            self.print = Button(self.root, text = "Print", justify = LEFT,anchor=W)
            self.print.place(x=0,y=60,height=30,width=100)
            
            self.logout = Button(self.root, text = "Log out", justify = LEFT,anchor=W, command=lambda: self.logoutofApp())
            self.logout.place(x=0,y=90,height=30,width=100)
            
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
        bList = []
        for i in range(len(patientList)):
            pstr = '{0:<10} {1:<13} {2:<13} {3:<10}'.format(patientList[i].fName, patientList[i].lName, patientList[i].dueDate, patientList[i].daysOverDue)
            
            #FONT has to be monospaced or it wont work
            b = Button(frame, text = pstr,anchor=W, justify=LEFT, width = 46, font = ('Consolas', 10), command=lambda i=i: self.showPatient(patientList[i].MRN))
            b.grid(row=i)
            bList.append(b)

    def showPatient(self, MRN):
        #hash map would be better
        for patient in self.queue:
            if patient.MRN == MRN:
                self.showSummary(patient)
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

        closeButton = Button(newWindow,text="Go Back",command= lambda:self.destroyPopOut(newWindow))
        closeButton.grid()

        newWindow.protocol("WM_DELETE_WINDOW",self.destroyPopOut(newWindow))

    def showSummary(self, patient):
        self.clearPatient()
        self.summary = 1
        self.summaryText = Label(self.root, text = "Patient Information:", font = (12))
        self.summaryText.place(x = 577.5, y = 102.5)
        
        self.pName = Label(self.root, text = "First Name: " + patient.fName)
        self.pName.place(x = 600, y = 135)

        expand = Button(self.root,text="Expand Patient",command=lambda:self.xPand(patient))
        expand.place(x=700,y=150)


    def clearPatient(self):
        if self.summary == 1:
            self.pName.destroy()
            
    def logoutofApp(self):
        self.togFileTab()
        print("Logging out")
        self.swapTO(loginScreen, None)
        print("Successful Log out!")

class Patient():
    def __init__(self, data):
        self.fName = data[0]
        self.lName = data[1]
        self.score = data[2]
        self.dueDate = data[3]
        self.MRN = data[4]
        self.daysOverDue = data[5]
           

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

        self.userName = "Test01"
        self.passWord = "Test02"

        menu = Label(window,text="Welcome to ICA! Please login!\n")
        menu.grid(sticky=W)

        nameLabel = Label(window,text="Username: ")
        passLabel = Label(window,text="Password: ")
        nameLabel.grid(row=2,sticky=W)
        passLabel.grid(row=3,sticky=W)

        self.nameENTRY = Entry(window)
        self.passENTRY = Entry(window,show="*")
        self.nameENTRY.grid(row=2,column=1)
        self.passENTRY.grid(row=3,column=1)

        loginBUTTON = Button(window,text="Login!",bg="blue",fg="white",command=self.verifyUser)
        loginBUTTON.grid(row=4,column=1)


    def verifyUser(self):
        name = self.nameENTRY.get()
        passWord = self.passENTRY.get()

        #Would hash and verify user with database here
        if name == self.userName and passWord == self.passWord:
            messagebox.showinfo("Login Successful!", "Welcome back " + str(name))
            self.swapTO(mainMenu, [self.userName])

        else:
            messagebox.showerror("Login Unsuccessful", "Username or Password is invalid")
            self.passENTRY.delete(0,END) #remove password

def main():
    window = Tk()
    window.resizable(0,0)
    #currentSCREEN = loginScreen(window, None)
    currentSCREEN = mainMenu(window, ["Jason Van Bladel"])
    window.mainloop()


main()
