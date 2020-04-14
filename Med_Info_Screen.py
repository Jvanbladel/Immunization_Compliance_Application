from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk,Image
from Patients import *
from tkinter import ttk
import ICA_super

class med_INFO_SCREEN(ICA_super.icaSCREENS):


    def __init__(self, window, Patient):
        super().__init__(window)
        self.root.geometry("800x730")
        self.bindKey("<Escape>",self.closeWindow)

        self.thisPatient = Patient
        self.currentUser = None
        self.insurance = None
        self.demoGraphics = None
        self.immunizationHistory = None


        #setup the notebook for patient screen
        self.patientNotebook = ttk.Notebook(self.root,width=800,height=670)




        self.demosPage = Frame(self.patientNotebook)


        self.servicePage = Frame(self.patientNotebook)
        self.contactPage = Frame(self.patientNotebook)
        self.immunizationHistory = Frame(self.patientNotebook)
        self.insurancePage = Frame(self.patientNotebook)

        self.patientNotebook.add(self.demosPage,text="Demographics")
        self.patientNotebook.add(self.servicePage, text="Service History")
        self.patientNotebook.add(self.contactPage, text="Outreach Report")
        self.patientNotebook.add(self.immunizationHistory,text="Immunizations")
        self.patientNotebook.add(self.insurancePage,text="Insurance")



        self.headlineFrame = LabelFrame(self.root, width=1100, height=30, bg="RoyalBlue3")
        self.headlineFrame.place(x=0, y=0)
        self.patientFULL = Patient.fName + " " + Patient.lName
        self.patientLabel = None
        self.originalHeadline() #displays the normal headline version on screen



        #will place the notebook under the main label
        self.patientLabel.update()
        notebookY = self.patientLabel.winfo_height()
        self.patientNotebook.place(x=0, y=notebookY)


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
        self.extensionFrame = None


        self.showDemos()
        self.showService()
        self.showOutReach()
        self.showImmunizationHistory()


        #hold service history listing
        self.serviceHistoryWidgets = []


        #will hold the previous location in the service page
        self.previousLocation = 0



    def showImmunizationHistory(self):

        immunizationGroups = ["Polio", "DTap/Td","HIB", "MMR", "HepB","Varicella",
                              "HepA","Pneumococcal","Infuenza","Meningococcal","Rotavirusz"]

        theFrame = self.immunizationHistory
        theFrame.update()
        theFrame.configure(bg="light blue")


        generalFont = ('consolas',12)
        Width = theFrame.winfo_width()
        Height = theFrame.winfo_height()


        header = Label(theFrame,text="List of immunizations we have on file for " + self.patientFULL,
                       font=generalFont)
        header.place(x=0,y=0)

        self.addImmunization(theFrame,30)

    def addImmunization(self,theFrame,startingY):

        generalFont = ('consolas',12)
        generalBG = "light blue"

        newImmunization = LabelFrame(theFrame,bg="light blue",width=790,height=150,highlightcolor="white",highlightthickness=2,bd=0)
        newImmunization.place(x=5, y=startingY)

        immunizationName = "ImmunizationName: DTap (Diphtheria, Tetanus, acellular Pertussis)"

        datesAdministered = ["8/9/2002", "7/16/1998", "10/10/1997", "8/15/1997", "6/17/1997"]

        administeredString = "Adminstered: "

        for date in datesAdministered:
            administeredString += (date + ", ")

        immunizationLabel = Label(newImmunization,text=immunizationName,font=generalFont,bg=generalBG)
        immunizationLabel.place(x=5,y=0)
        immunizationLabel.update()

        nextY = immunizationLabel.winfo_y() + immunizationLabel.winfo_height() + 15

        administeredLabel = Label(newImmunization,text=administeredString,font=generalFont,bg=generalBG)
        administeredLabel.place(x=5,y=nextY)
        administeredLabel.update()

        nextY = administeredLabel.winfo_height() + administeredLabel.winfo_y() + 30


        learnMoreButton = Button(newImmunization, text="Learn more", font=generalFont)
        learnMoreButton.place(x=5,y=nextY)







    def label_and_TextDEP(self,frame,labelText,xPos,yPos,insertedText): # this should create a label and place the text beneath it

        newLabel = Label(frame,text = labelText,font = ('consolas',12),bg="light blue")
        newLabel.place(x=xPos,y=yPos)
        newLabel.update()


        newText = Text(frame,width=len(insertedText),height=1)
        newText.place(x=xPos,y=yPos + newLabel.winfo_height() + 2)



    def showDemosDEP(self): # uses self.demosPage for display

        self.extensionGuarantor()
        self.demosPage.update()
        self.demosPage.config(bg="light blue")

        Width= self.demosPage.winfo_width()
        Height = self.demosPage.winfo_height()

        patientFrame = LabelFrame(self.demosPage,text="<Patient>",width=Width - 10,height=80,bg="light blue",
                                       highlightcolor="white",highlightthickness=2,font=('consolas',12),bd=0,labelanchor="n")
        patientFrame.place(x=5,y=5)
        patientFrame.grid_propagate(False)

        self.label_and_Text(patientFrame,"Lastname",0,0,self.thisPatient.lName)

        self.label_and_Text(patientFrame,"Firstname",0,4,self.thisPatient.fName)

        self.label_and_Text(patientFrame,"Middle Initial",0,8,"Init")

        self.label_and_Text(patientFrame, "Prefix", 0, 12, "Ms.")

        self.label_and_Text(patientFrame, "NickName", 0,16, "nick")

        patientFrame.grid_columnconfigure(4, minsize=125)
        patientFrame.grid_rowconfigure(2,minsize=25)


        demoFrame = LabelFrame(self.demosPage,text="<Demographics>",width=Width,height=80,bg="light blue",
                                       highlightcolor="white",highlightthickness=2,font=('consolas',12),bd=0,labelanchor="n")
        demoFrame.place(x=0,y=100)
        demoFrame.grid_propagate(False)


        self.label_and_Text(demoFrame, "Sex", 0, 0, "Female")
        self.label_and_Text(demoFrame, "DOB", 0, 2, "2/20/2013")
        self.label_and_Text(demoFrame, "Pref. Language", 0, 4, "English")
        self.label_and_Text(demoFrame, "Race", 0, 6, "Caucasian")
        self.label_and_Text(demoFrame, "Ethnicity", 0, 8, "White")
        self.label_and_Text(demoFrame, "Age", 0, 10, "50")

        demoFrame.grid_columnconfigure(4, minsize=125)
        demoFrame.grid_rowconfigure(2, minsize=25)

        addressFrame = LabelFrame(self.demosPage,text="<Address>",width=Width,height=125,bg="light blue",
                                       highlightcolor="white",highlightthickness=2,font=('consolas',12),bd=0,labelanchor="n")
        addressFrame.place(x=0,y=175)
        addressFrame.grid_propagate(False)

        self.label_and_Text(addressFrame,"Street 1",0,0,"1234 random Street")
        self.label_and_Text(addressFrame, "Street 2", 4, 0, "1234 random Street 2")
        self.label_and_Text(addressFrame, "Zipcode", 0, 2, "00000")
        self.label_and_Text(addressFrame, "City", 0, 3, "Pacific City")
        self.label_and_Text(addressFrame, "State", 4, 2, "CA")
        self.label_and_Text(addressFrame, "County", 4,3, "randomCounty")
        self.label_and_Text(addressFrame, "Country", 0,4, "Some Country")

        addressFrame.grid_columnconfigure(4, minsize=125)
        addressFrame.grid_rowconfigure(2, minsize=25)

        contactFrame = LabelFrame(self.demosPage,text="<Contact>",width=Width,height=175,bg="light blue",
                                       highlightcolor="white",highlightthickness=2,font=('consolas',12),bd=0,labelanchor="n")
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
        self.contactNotes.place(x=230,y=125)
        self.contactNotes.insert('end',"Notes about contacting this patient here")
        self.contactNotes.configure(state=DISABLED)

        contactFrame.grid_columnconfigure(4, minsize=100)
        contactFrame.grid_rowconfigure(2, minsize=50)

        GuarantorButton = Button(contactFrame, text = "Guarantor Info",command= self.extensionGuarantor)
        GuarantorButton.place(x=400,y=0)



    def showDemos(self): # secondary attempt at the demos page

        '''
        self.demosPage.update() # will now contain the width and height
        Width = self.demosPage.winfo_width()
        Height = self.demosPage.winfo_height()


        self.demosFrame = Frame(self.demosPage, relief=GROOVE, bd=1,bg = "light blue")
        self.demosFrame.place(x=0, width=Width, y=0, height=Height)

        self.demosCanvas = Canvas(self.demosFrame,bg="light blue",highlightbackground="light blue")
        self.theFrame = Frame(self.demosCanvas,bg="light blue")
        self.demosScrollBar = Scrollbar(self.demosFrame, orient="vertical", command=self.demosCanvas.yview)
        self.demosCanvas.configure(yscrollcommand=self.demosScrollBar.set)
        self.demosScrollBar.pack(side="right", fill="y")
        self.demosCanvas.pack(side="left")
        self.demosCanvas.create_window((0, 0), window=self.theFrame, anchor='nw')
        self.theFrame.bind("<Configure>", self.demosScrollFunction)



        emptyLabel = Label(self.theFrame,anchor=W,justify=LEFT)
        emptyLabel.pack()

        patientDetails = LabelFrame(self.theFrame,text="<Patient Details>",bg = "light blue",width=300,height=200)
        patientDetails.pack()



        labels = ["Last Name", "First Name"]


        for label in labels:

            newLabel = Label(patientDetails,text = label,bg = "light blue")
            newLabel.grid(row=0,column=0)


        '''

        self.demosPage.update()  # will now contain the width and height
        Width = self.demosPage.winfo_width()
        Height = self.demosPage.winfo_height()

        self.demosPage.config(bg="light blue")


        # this will set up the patient frame
        self.patientFrame = LabelFrame(self.demosPage,text = "Patient Demographics",width=Width - 10,height=250,bg="light blue",
                                       highlightcolor="white",highlightthickness=2,font=('consolas',12),bd=0,labelanchor="n")
        #patientFrame.place(x=0,y=0)
        self.patientFrame.place(x=5,y=5)
        self.patientFrame.update()


        # contains a list of labels to be added for patient details frame
        patientDetailsList = ["Last Name","First Name","Nickname","Middle Name(s)","Prefix","Sex"]

        PatientDemographicsList = ["Last Name","First Name","Nickname","Middle Name(s)","Prefix","Sex",
                                   "D.O.B","Age", "Race", "Ethnicity","Pref. Language", "Deceased Status"]

        staticDetails = ["Random", "Random", "Rand", "Random", "No Prefix", "Male",
                         "1/23/1991","29","Insert Race","Insert Ethnicity", "English", "Alive"]




        detailsPosY = 30
        detailsPosXIncrease = 0
        for index in range(len(PatientDemographicsList)):

            if index == 6: #sets new postion for next row
                detailsPosY = 30
                detailsPosXIncrease = 350


            newLabel = Label(self.patientFrame,text = PatientDemographicsList[index],font=('consolas',12),bg="light blue")
            newLabel.place(x=5 + detailsPosXIncrease,y=detailsPosY)
            newLabel.update()


            #display the textboxes
            newTextBox = Text(self.patientFrame,width=20,height=1)
            newTextBox.place(x=150 + detailsPosXIncrease,y=detailsPosY)
            newTextBox.insert('end',staticDetails[index])
            newTextBox.configure(state=DISABLED)

            detailsPosY += 30


        self.addressFrame = LabelFrame(self.demosPage,text="Patient Address Details",width=Width-10,height=100,bg="light blue",
                                       highlightcolor="white",highlightthickness=2,font=('consolas',12),bd=0,labelanchor="n")

        self.addressFrame.place(x=5,y=self.patientFrame.winfo_y() + self.patientFrame.winfo_height() + 5)
        self.addressFrame.update()

        addressLabels = ["Street 1", "Street 2", "City", "State", "Zipcode", "County", "Country"]
        staticAddress = ["12345 Randomstreet Circle", "5783 anotherstreet drive","Stockton", "CA","32131",  "Some County", "United States"]

        addedLabels = []

        for label in addressLabels:
            newLabel = Label(self.addressFrame, text= label, bg="light blue", font=('consolas', 12))
            newLabel.update()
            addedLabels.append(newLabel)



        addedLabels[0].place(x=5,y=5)

        addedLabels[1].place(x=5,y=35)

        addedLabels[2].place(x=300,y=5)

        addedLabels[3].place(x=300,y=35)

        addedLabels[4].place(x=425,y=5)

        addedLabels[5].place(x=425,y=35)

        addedLabels[6].place(x=550,y=5)

        yPos = 5
        for index in range(len(staticAddress)):

            if yPos > 35:
                yPos = 5

            addedLabels[index].update()
            xPos = addedLabels[index].winfo_x() + addedLabels[index].winfo_width() + 1


            addedText = staticAddress[index]

            newText = Text(self.addressFrame,width=len(addedText),height=1)
            newText.place(x=xPos,y=yPos)
            newText.insert('end',addedText)
            newText.configure(state=DISABLED)

            yPos += 30



        #set up the notebook for bottom of demographics
        self.demosNoteBook = ttk.Notebook(self.demosPage,width = Width - 25, height = Height - self.patientFrame.winfo_height() - self.addressFrame.winfo_height(),padding = 5)
        self.demosNoteBook.place(x=5,y= self.addressFrame.winfo_height() + self.addressFrame.winfo_y()+ 5)


        self.contactINFO = Frame(self.demosNoteBook,bg="light blue")
        self.demosNoteBook.add(self.contactINFO,text="Contact Information")


        
        self.guarantorInformation = Frame(self.demosNoteBook,bg="light blue")
        self.demosNoteBook.add(self.guarantorInformation,text="Guarantor Information")


        self.demoOtherFrame = Frame(self.demosNoteBook)
        self.demoOtherFrame.config(bg="light blue")
        self.demosNoteBook.add(self.demoOtherFrame, text="Other")




        #contact information displayed below here

        contactLabels = ["Phone Number","Phone Extension","Phone Type","Email Address", "Preferred Contact",
                         "Interpreter Required"]

        staticContactINFO = ["123-456-789 ", "+1 (916)","Work","r_Andom@u.pacific.edu", "Email", "No"]


        xPos = 5
        yPos = 5
        self.contactINFO.update()
        for index in range(len(contactLabels)):

            labelInsert = contactLabels[index]
            textInsert = staticContactINFO[index]




            newLabel = Label(self.contactINFO,text=labelInsert,font=('consolas',12),bg="light blue")
            newLabel.place(x=xPos,y=yPos)
            newLabel.update()


            textX = newLabel.winfo_width() + newLabel.winfo_x() + 5
            textY = newLabel.winfo_y()

            newText = Text(self.contactINFO,width=len(textInsert),height = 1,font=('consolas',12))
            newText.insert('end',textInsert)
            newText.configure(state=DISABLED)
            newText.place(x=textX,y=textY)
            newText.update()


            yPos += 45


        contactNotesLabel = Label(self.contactINFO,text="Contact Notes",bg="light blue",font=('consolas',12))
        contactNotesLabel.place(x=500,y=5)
        contactNotesLabel.update()

        contactNotesText = Text(self.contactINFO,width=40,height=13,padx=5)
        contactNotesText.place(x=400,y=contactNotesLabel.winfo_y() + contactNotesLabel.winfo_height() + 5)
        contactNotesText.insert('end',"This patient is a member of Professor Gao's COMP 129 class!")
        contactNotesText.configure(state=DISABLED)
        contactNotesText.update()


        #guarantor information

        guarantorInformationlabels = ["First Name", "Last Name","Middle Initial", "GuarantorGender"]



        headerLabel = Label(self.demoOtherFrame,text="These are just here for testing purposes")
        headerLabel.pack()

        guarantorButton = Button(self.demoOtherFrame,text="Guarantor Extension before update",command=self.extensionGuarantor)
        guarantorButton.pack()


        emailButton = Button(self.demoOtherFrame,text="Email Extension before update",command=self.extensionEmail)
        emailButton.pack()





    def extensionGuarantor(self): # display the Garantour in the extension

        self.addExtension()


        #obtain information here


        generalFont = ('consolas',10) # general font used for the labels


        # extension title
        testLabel = Label(self.extensionFrame,text="Guarantor Information",relief=GROOVE, font=('consolas',19))
        testLabel.place(x=0,y=0)

        informationLabel = ["First name: ", "Last Name: ", "Middle Initial: ",
                            "Source System: ", "Created Date Time: ", "Created Person ID: ",
                            "Update Date Time: ", "Update Person ID: "]

        staticInfo = ["Colton", "Remmert", "J", '<Insert Here>', "<Insert Here>", "<Insert Here>",
                      "<Insert Here>", "<Insert Here>", "<Insert Here>"]


        self.guarantorLabels = {} # contains labels that are connected to label text/ginfo

        xPos = 0
        yPos = 50
        for index in range(len(informationLabel)): # set the page up

            formatText = informationLabel[index] # text to go onto the first label
            ourText = staticInfo[index] # this Guarantor's text

            newLabel = Label(self.extensionFrame, text=formatText, font=generalFont, relief=GROOVE)
            newLabel.place(x=xPos, y=yPos)

            newLabel.update()

            formatWidth = newLabel.winfo_width() + 15

            gINFO = Label(self.extensionFrame,text = ourText, font = generalFont)
            gINFO.place(x=formatWidth,y=yPos)

            yPos += 50

            self.guarantorLabels[formatText] = newLabel # store our labels connected to the formattedText

        closeButton = Button(self.extensionFrame,text = "Close Guarantor Example Page", command= self.removeExtension)
        closeButton.place(x=50,y=450)

    def label_and_Text(self,frame,labelText,labelRow,labelCol,boxText):

        lNameLabel = Label(frame, text='{0:<10}'.format(labelText),font=('consolas',11),bg="light blue")
        lNameLabel.grid(row=labelRow, column=labelCol,padx=10)

        patientLname = Text(frame, width=len(boxText), height=1,padx=5,font=('consolas',11))
        patientLname.insert('end', boxText)
        patientLname.configure(state=DISABLED)
        patientLname.grid(row=labelRow+2, column=labelCol)

    def putFormat(self):

        formatString = '{0:<20}{1:<20}{2:<17}{3:<20}{4:<10}'.format("Service ID", "Immunization",
                                                                   "Administered?", "Service Date", "Dose Number")

        self.formatLabel = Label(self.servicePage, text=formatString, font=('Consolas', 11)
                            , relief="raised",width=800,height=2)
        self.formatLabel.pack()
        self.formatLabel.update()

    def showService(self): # uses servicePage Canvas for display

        self.putFormat()

        self.newFrame = Frame(self.servicePage, relief=GROOVE, bd=1)
        self.newFrame.place(x=0, width=800, y=40, height=660)

        self.canvas = Canvas(self.newFrame)
        self.newnewFrame = Frame(self.canvas)
        self.myScrollBar = Scrollbar(self.newFrame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.myScrollBar.set)
        self.myScrollBar.pack(side="right", fill="y")
        self.canvas.pack(side="left",expand=True,fill="both")
        self.canvas.create_window((0, 0), window=self.newnewFrame, anchor='nw')
        self.newnewFrame.bind("<Configure>", self.scrollFunction)
        self.newnewFrame.configure(bg="light blue")

        # format Service ID, Immunization Name, Compliance, Service Date, Extra Tab?

        immunizations = ["Flu shot", "Menengitis", "Tetanus", "Allergy?"]
        choice = ["Yes","No"]


        self.displayServiceHistory()

    def displayServiceHistory(self): # will create a list of buttons that hold links to service info

        if  not self.myScrollBar.winfo_ismapped():  # will repack scroll bar and formatLabel
            self.formatLabel.forget()
            self.putFormat()
            self.formatLabel.pack()
            self.myScrollBar.pack(side="right", fill="y")

        for index in range(30): # This is where we would queue the database for information. Probably modify to only do once
            serviceID = "E15" + str(index)
            patientINFO = [serviceID, "Immunization", "Yes", "1/1/2000", 2]
            buttonINFO = self.formatService(patientINFO)

            self.serviceHistory = [] # holds all service
            button = Button(self.newnewFrame, text = buttonINFO,anchor=W,justify=LEFT, width = 100, font=('Consolas', 11))
            button.grid(row=index)
            button.configure(command=lambda x=patientINFO: self.loadService(x))
            self.serviceHistory.append(button)

    def formatService(self,patientService): # will format the buttons to be displayed in the service history

        # format Service ID, Immunization Name, Compliance, Service Date, Extra Tab?
        #formatString = '{0:<7}{1:<10}{2:<20}{3:<17}{4:<20}{5:<20}'.format("",patientService[0],patientService[1],patientService[2]
        #                                                          ,patientService[3],patientService[4])


        # new format has spacing to make the design look neater
        formatString = '{0:<7}{1:<10}{2:<8}{3:<20}{4:<5}{5:<14}{6:<0}{7:<20}{8:<2}{9:<20}'.format("",patientService[0],"",patientService[1],
                                                                                                  "",patientService[2],"",patientService[3],
                                                                                                  "",patientService[4])

        return formatString

    def scrollFunction(self,event): # this will scroll the service canvas

        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=500,height=500)


    def hideServiceHistory(self): # will hide the previous screen to allow for more info to be displayed

        #self.formatLabel.config(text="") # clear the label
        for widget in self.newnewFrame.winfo_children():
            widget.destroy()



    def loadServiceHistory(self): # will load patient service history from the database
                                  # I have a temp format here for now though

        serviceID = 1
        immunizations = ["Immunization 1", "Immunization 2"]
        compliance = ["Yes", "No"]
        ServiceDate = ["2/1/2013"]
        Doses = [1,2]
        patientService = [serviceID,immunizations[1], compliance[0],ServiceDate, Doses[0]]

        self.formatService(patientService)

    def loadService(self,patientINFO): # will diplay specific service in expansion window

        '''
        self.checkExtension() # will close previous page

        label = Label(self.extensionFrame,text = "Service #" + str(patientINFO[0]) ,font = ('consolas', 14),relief=GROOVE) # will display the specific service
        label.place(x=0,y=0)


        serviceDateLabel = Label(self.extensionFrame,text = "Service Date: ",font = ('consolas', 10))
        serviceDateLabel.place(x=0,y=40)

        serviceDate = Text(self.extensionFrame,width = len(patientINFO[3]),height = 1,padx =5)
        serviceDate.place(x=85,y=40)
        serviceDate.insert('end',patientINFO[3])
        serviceDate.configure(state=DISABLED)

        patientLname = Text(frame, width=len(boxText), height=1, padx=5)
        patientLname.insert('end', boxText)
        patientLname.configure(state=DISABLED)
        patientLname.grid(row=labelRow + 2, column=labelCol)
        '''

        #does basic setup for the service screen
        self.hideServiceHistory()
        self.formatLabel.configure(text="Showing details for Service #" + patientINFO[0],font=('consolas',12))
        self.myScrollBar.pack_forget()
        self.canvas.yview_moveto(0)


        #general widget settings
        generalFont = ('consolas', 12)
        generalBG = "light blue"
        theFrame = self.newnewFrame



        #static data that is used during developement
        DOS = "1/1/2000"
        receivedImmunization = "diphtheria, tetanus toxoids, and acellular pertussis"
        immunizationABBV = "DTaP"
        allergicReactions = "N/A"

        xPos = 200
        yPos = 10
        increment = 20
        textX = 400

        serviceDetailsHeader = Label(theFrame,text="Service Details",width= theFrame.winfo_width(),height = 1,bg="RoyalBlue3",font=generalFont,fg="white",anchor=W)
        serviceDetailsHeader.place(x=0,y=0)
        serviceDetailsHeader.update()


        yPos = serviceDetailsHeader.winfo_height() + serviceDetailsHeader.winfo_y() + increment


        serviceDateLabel = Label(theFrame,text="Date of Service",bg=generalBG,font=generalFont)
        serviceDateLabel.place(x=xPos,y=yPos)
        serviceDateLabel.update()



        serviceDateText = Text(theFrame,width=len(DOS),height = 1,font=generalFont)
        serviceDateText.place(x=textX,y=yPos)
        serviceDateText.insert('end',DOS)
        serviceDateText.configure(state=DISABLED)

        yPos = serviceDateLabel.winfo_height() + serviceDateLabel.winfo_y() + increment


        immunizationLabel = Label(theFrame,text="Immunizations Received",bg=generalBG,font=generalFont)
        immunizationLabel.place(x=xPos,y=yPos)
        immunizationLabel.update()


        immuX = immunizationLabel.winfo_width() + immunizationLabel.winfo_x() + 5


        immuReceived = StringVar(theFrame)
        immuReceived.set("DTaP")


        immunizationsReceived = Combobox(theFrame,values=["DTaP","Flu","HIV"])
        immunizationsReceived.set("DtaP")
        #immunizationsReceived = OptionMenu(theFrame,immuReceived,'Flu',"HIV")
        immunizationsReceived.place(x=immuX,y=yPos)
        immunizationsReceived.update()


        immuXtension = immunizationsReceived.winfo_width() + immunizationsReceived.winfo_x() + 10
        extendImmunizationButton = Button(theFrame,text="Information on \nSelected Immunization",
                                        command=self.extensionImmunization)
        extendImmunizationButton.place(x=immuXtension,y=yPos)


        yPos = immunizationLabel.winfo_y() + immunizationLabel.winfo_height() + increment


        completionStatusLabel = Label(theFrame,text="Completion Status",bg=generalBG,font=generalFont)
        completionStatusLabel.place(x=xPos,y=yPos)
        completionStatusLabel.update()


        completionX = completionStatusLabel.winfo_x() + completionStatusLabel.winfo_width() + 5

        completionStatusText = Text(theFrame,width=15,font=generalFont,height=1)
        completionStatusText.place(x=completionX,y=yPos)
        completionStatusText.configure(state=DISABLED)


        yPos = completionStatusLabel.winfo_y() + completionStatusLabel.winfo_height() + increment


        informationSourceLabel = Label(theFrame,text="Information Source",bg=generalBG,font=generalFont)
        informationSourceLabel.place(x=xPos,y=yPos)
        informationSourceLabel.update()

        informationX = informationSourceLabel.winfo_width() + informationSourceLabel.winfo_x() + 5

        informationSourceText = Text(theFrame,width=15,font=generalFont,height=1)
        informationSourceText.place(x=informationX,y=yPos)
        informationSourceText.configure(state=DISABLED)


        yPos = informationSourceLabel.winfo_y() + informationSourceLabel.winfo_height() + increment

        sourceSystemLabel = Label(theFrame,text="Source System",bg=generalBG,font=generalFont)
        sourceSystemLabel.place(x=xPos,y=yPos)
        sourceSystemLabel.update()

        sourceX = sourceSystemLabel.winfo_x() + sourceSystemLabel.winfo_width() + 5


        sourceSystemText = Text(theFrame,width=15,font=generalFont,height=1)
        sourceSystemText.place(x=sourceX,y=yPos)
        sourceSystemText.configure(state=DISABLED)




        yPos = sourceSystemLabel.winfo_y() + sourceSystemLabel.winfo_height() + increment


        reactionsHeader = Label(theFrame, text="Reactions", width=theFrame.winfo_width(), height=1,
                                     bg="RoyalBlue3", font=generalFont, fg="white", anchor=W)

        reactionsHeader.place(x=0,y=yPos + 30)
        reactionsHeader.update()

        yPos = reactionsHeader.winfo_height() + reactionsHeader.winfo_y() + increment

        allergicReactionsLabel = Label(theFrame,text="Allergic Reactions",bg=generalBG,font=generalFont)
        allergicReactionsLabel.place(x=xPos,y=yPos)
        allergicReactionsLabel.update()



        allergicReactionsText = Text(theFrame,width=30,height=3)
        allergicReactionsText.place(x=textX,y=yPos)
        allergicReactionsText.configure(state=DISABLED)
        allergicReactionsText.update()

        yPos = allergicReactionsText.winfo_y() + allergicReactionsText.winfo_height() + increment


        serviceProviderHeader = Label(theFrame,text="Service Provider",bg="RoyalBlue3",fg="white",
                                      font=generalFont,anchor=W,
                                      width=theFrame.winfo_width(),height=1)
        serviceProviderHeader.place(x=0,y=yPos)
        serviceProviderHeader.update()


        yPos = serviceProviderHeader.winfo_height() + serviceProviderHeader.winfo_y() + increment

        serviceProviderLabel = Label(theFrame,text="Provider Name",bg=generalBG,font=generalFont)
        serviceProviderLabel.place(x=xPos,y=yPos)
        serviceDateLabel.update()

        providerX = serviceDateLabel.winfo_x() + serviceDateLabel.winfo_width() + 10


        serviceProviderText = Text(theFrame,width=20,height=1,font=generalFont)
        serviceProviderText.place(x=providerX,y=yPos)
        serviceProviderText.update()

        yPos += (serviceProviderText.winfo_height() + increment + 50)


        returnButton = Button(theFrame,text="Back to Service History",bg="RoyalBlue3",fg="white",font=generalFont,
                              command=self.displayServiceHistory)
        returnButton.place(x=xPos,y=yPos)





    def extensionImmunization(self): # pass detailed immunization information here and place on extension window

        self.addExtension()
        self.checkExtension()
        theFrame = self.extensionFrame # easier to reference
        generalFont = ('consolas', 12)

        immunizationName = "DTaP (Diphtheria, Tetanus, acellular Pertussis)"
        immunizationName2 = "HBV (Hepatitis B)"


        immunizationHeader = Label(theFrame,text=immunizationName,font=generalFont,wraplengt=300)
        immunizationHeader.place(x=50,y=0)



    def showOutReachDEP(self): # uses patient Canvas for display

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

        contactNotes = Text(self.contactPage,width=30,height=10,padx=5)
        contactNotes.place(x=0,y=175)
        contactNotes.insert('end',"Notes about contacting this patient here")

        outreachNotesLabel = Label(self.contactPage, text="Outreach Notes")
        outreachNotesLabel.place(x=350, y=150)

        self.outreachNotes = Text(self.contactPage, width=27, height=10,padx=5)
        self.outreachNotes.place(x=275, y=175)
        self.outreachNotes.insert('end',"Patient did not want an to schedule an appointment")


        #update widget positions for tkinter
        notesLabel.update()
        self.outreachNotes.update()
        #self.contactNotes.update()
        outreachNotesLabel.update()

        contactSubmitX = notesLabel.winfo_x()
        SubmitY = self.outreachNotes.winfo_y() + self.outreachNotes.winfo_height() + 10
        outreachSubmitX = outreachNotesLabel.winfo_x()


        contactNotesButton = Button(self.contactPage,text="Submit Changes")
        contactNotesButton.place(x=contactSubmitX,y=SubmitY)

        outreachNotesButton = Button(self.contactPage,text="Submit Changes")
        outreachNotesButton.place(x=outreachSubmitX,y=SubmitY)


        #contact Method Frame
        contactMethodFrame = LabelFrame(self.contactPage, text="<Method of contact>",width=500,height=100)
        contactMethodFrame.place(x=0,y=400)
        contactMethodFrame.grid_propagate(False)

        emailPatient = Button(contactMethodFrame,text="Email Patient",command=self.extensionEmail)
        emailPatient.place(x=25,y=25)


    def showOutReach(self): # newer version of outreaching to patients

        # Setup for  the contact page
        self.contactPage.update()
        Width = self.contactPage.winfo_width()


        self.contactPage.configure(bg="light blue")


        # initialized vars
        theFrame = self.contactPage


    def getPatientHistory(self):
        pass

    def getPatientDemographics(self): # need to load in Patient details
        pass

    def closeWindow(self,event):
        self.root.destroy()

    def extensionEmail(self,savedText=None): # will display extension for emailing patient

        self.addExtension()

        tempLabel = Button(self.extensionFrame,text="Close extension",command= self.removeExtension)
        tempLabel.place(x=200,y=0)

        displayLabel = Label(self.extensionFrame,text="To:" + self.patientFULL ,font = ('Consolas', 14),relief="groove")
        displayLabel.place(x=0,y=30)

        templateLabel = Label(self.extensionFrame,text="<Email Template>")
        templateLabel.place(x=0,y=75)

        self.emailText = Text(self.extensionFrame,width=35,height=15,padx=10)
        self.emailText.place(x=0,y=100)

        buttonFrame = LabelFrame(self.extensionFrame,text="<Email Options>",width=300,height=150)
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


    def addExtension(self): # add extension to extended patient screen

        if self.extensionFrame is not None: # checks if we already have an extension open
            self.checkExtension()  # will close previous page
            return

        self.root.geometry("1100x730")
        self.extensionFrame = LabelFrame(self.root, width=300, height=670)
        self.extensionFrame.place(x=800, y=50)
        self.extensionHeadline()

    def headlineExists(self):

        if self.patientLabel is not None:
            self.patientLabel.destroy()

    def extensionHeadline(self):

        self.headlineExists()

        # format; FULL Name, Gender, Age <years> DOB, MRN
        self.patientLabelText = '{0:<30}{1:<20}{2:<20}{3:<20}{4:<20}'.format("PATIENT:" + self.patientFULL,
                                                                             "GENDER: Female", "AGE:50 ",
                                                                             "DOB:3/21/2013", "MRN:30")

        self.patientLabel = Label(self.headlineFrame, text=self.patientLabelText, font=('Consolas', 14),
                                  bg="RoyalBlue3", fg="white")
        self.patientLabel.place(x=0, y=0)

    def originalHeadline(self):

        self.headlineExists()

        # format; FULL Name, Gender, Age <years> DOB, MRN
        self.patientLabelText = '{0:<30}{1:<17}{2:<10}{3:<15}{4:<10}'.format("PATIENT:" + self.patientFULL,
                                                                             "GENDER: Female", "AGE:50 ",
                                                                             "DOB:3/21/2013", "MRN:30")

        self.patientLabel = Label(self.headlineFrame, text=self.patientLabelText, font=('Consolas', 14),
                                  bg="RoyalBlue3", fg="white")
        self.patientLabel.place(x=0, y=0)



    def removeExtension(self): # remove extension to extended patient screen

        self.clearExtension()
        self.root.geometry("800x730")
        self.extensionFrame.destroy()
        self.extensionFrame = None
        self.originalHeadline()

    def checkExtension(self): # checks if there is a prexisting service open

        if self.extensionFrame is None: # Extension does not exist
            return

        self.clearExtension()

    def clearExtension(self): # will clear the extension Frame

        for widget in self.extensionFrame.winfo_children():
            widget.destroy()




