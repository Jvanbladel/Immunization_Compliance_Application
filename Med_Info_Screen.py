from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk,Image
from Patients import *
from tkinter import ttk
import ICA_super

class med_INFO_SCREEN(ICA_super.icaSCREENS):


    def __init__(self, window, Patient, SQL):
        super().__init__(window, SQL)
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

