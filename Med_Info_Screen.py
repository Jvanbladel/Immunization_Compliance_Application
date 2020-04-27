from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk,Image
from Patients import *
from tkinter import ttk
import ICA_super
import SQLConnection
import webbrowser
from datetime import date

class med_INFO_SCREEN(ICA_super.icaSCREENS):


    def __init__(self, window, Patient, user):
        super().__init__(window)
        self.root.geometry("850x730")
        self.bindKey("<Escape>",self.closeWindow)

        self.thisPatient = Patient
        self.user = user
        self.demoGraphics = self.SQL.getDemographics(Patient.patientID)
        self.ContactNotes = self.SQL.getContactNotes(Patient.patientID)
        self.InsuranceTab = self.SQL.getInsuranceTab(Patient.patientID)
        self.OutreachDetails = self.SQL.getOutreachDetails(Patient.patientID)
        self.ImmunizationEducation = self.SQL.getImmunizationEducation(Patient.patientID)
        #print(self.demoGraphics.address)
        #print(self.demoGraphics.demographics)
        #print(self.demoGraphics.contact)

        self.currentUser = None
        self.insurance = None
        #self.demoGraphics = None
        self.immunizationHistory = None


        #setup the notebook for patient screen
        self.patientNotebook = ttk.Notebook(self.root,width=850,height=670)


        self.demosPage = Frame(self.patientNotebook)


        self.servicePage = Frame(self.patientNotebook)
        self.contactPage = Frame(self.patientNotebook)
        self.immunizationHistory = Frame(self.patientNotebook)
        #self.insurancePage = Frame(self.patientNotebook)

        self.patientNotebook.add(self.demosPage,text="Demographics")
        self.patientNotebook.add(self.servicePage, text="Service History")
        self.patientNotebook.add(self.contactPage, text="Outreach Report")
        self.patientNotebook.add(self.immunizationHistory,text="Immunizations")
        #self.patientNotebook.add(self.insurancePage,text="Insurance")



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


        self.generateImmunizationLinks() # generates the links needed for the immunizations


        # setup for the page
        theFrame = self.immunizationHistory
        theFrame.update()
        theFrame.configure(bg="light blue")

        generalFont = ('consolas',12)
        Width = theFrame.winfo_width()
        Height = theFrame.winfo_height()

        self.immunizationFrame = Frame(theFrame)
        self.immunizationFrame.configure(bg="light blue")
        self.immunizationCanvas = Canvas(self.immunizationFrame)
        self.immunizationCanvas.configure(bg="light blue")
        self.scrollableFrame = Frame(self.immunizationCanvas)
        self.immunizationScrollbar = Scrollbar(self.immunizationFrame,orient="vertical"
                                               ,command=self.immunizationCanvas.yview)
        self.immunizationCanvas.configure(yscrollcommand=self.immunizationScrollbar.set)

        # self.immunizationFrame.pack()
        self.immunizationFrame.place(x=0, y=0, width=850, height=800)
        self.immunizationCanvas.pack(side="left", fill="both", expand=True)
        self.immunizationScrollbar.pack(side="right", fill="y")
        self.immunizationCanvas.update()

        self.immunizationCanvas.create_window((0, 0), window=self.scrollableFrame, anchor="nw")

        self.scrollableFrame.bind("<Configure>", lambda e: self.immunizationCanvas.configure(
           scrollregion=self.immunizationCanvas.bbox("all"), width=850,height=800)
        )



        # default box that is placed in every immunization history page
        generalInformationFrame = LabelFrame(self.immunizationCanvas, text="General information about the flu vaccine"
                                             , width=self.immunizationCanvas.winfo_width() - 10, height=100, bg="light blue",
                                             highlightcolor="white", highlightthickness=2,
                                             font=('consolas', 12), bd=0, labelanchor="n")

        generalInformationFrame.place(x=5, y=5)
        generalInformationFrame.update()

        generalInformationButton = Button(generalInformationFrame, text="Why to get Vaccinated",
                                          font=generalFont,
                                          command=lambda: self.openWebPage(
                                              "Why is it important to get annual flu vaccine?"))
        generalInformationButton.place(x=100, y=20)

        generalInformationButton2 = Button(generalInformationFrame,text= "Benefits of the vaccine",font=generalFont,
                                           command=lambda: self.openWebPage("What are the benefits of flu vaccination"))
        generalInformationButton2.place(x=400,y=20)
        nextY = generalInformationFrame.winfo_height() + generalInformationFrame.winfo_y() + 5


        # add more information to the generalInformation box here if needed
        immunizationGroups=[]
        datesAdministered=[]
        SQL = self.SQL
        serviceHistory = (SQL.getServiceDetails(self.thisPatient.patientID))
        #print(serviceHistory.ImmunizationID)

        serviceHistory = serviceHistory.groupby(['ImmDisplayDescription'])['PatientLastVisitDate'].apply(', '.join)
        datesAdministered = serviceHistory.tolist()
        print("169")
        print(datesAdministered)
        immunizationGroups = serviceHistory.index

        #print(immunizationGroups)
        # Queue the database here for the list of the immunization names
        '''immunizationGroups = ["Influenza Vaccine Prev Free 0.25 ml", "Influenza Vaccine quad split virus 0.5 ml",
                              "Influenza Vaccine quad split virus Prev Free ID Use",
                              "Influenza Vaccine quad split virus Prev Free 0.25 ml"]'''


        # Queue the database for the list of dates administered here
        '''datesAdministered = [["8/9/2002", "7/16/1998", "10/10/1997", "8/15/1997", "6/17/1997"],
                             ["3/9/1998","8/15/1997","6/17/1997"],
                             ["7/16/1998","10/10/1997", "8/15/1997", "6/17/1997"],
                             ["7/16/1998","10/10/1997", "8/15/1997", "6/17/1997"],
                             ["7/16/1998","10/10/1997", "8/15/1997", "6/17/1997"],
                             ["7/16/1998","10/10/1997", "8/15/1997", "6/17/1997"],
                             ["7/16/1998","10/10/1997", "8/15/1997", "6/17/1997"]]'''


        staticURL = "www.google.com"


        #nextY = 5
        addedFrames = []
        canvasWidth = self.immunizationCanvas.winfo_width()

        for index in range(len(immunizationGroups)):

            #staticURL = self.switchURL[immunizationGroups[index]]
            staticURL = ""
            newFrame = self.addImmunization(self.immunizationCanvas,nextY,canvasWidth,immunizationGroups[index],
                                 datesAdministered[index],staticURL)
            newFrame.update()

            addedFrames.append(newFrame)

            nextY = newFrame.winfo_height() + newFrame.winfo_y() + 10


    def addImmunization(self,theFrame,startingY,canvasWidth,immunizationName,datesAdministered,url):

        generalFont = ('consolas',12)
        generalBG = "light blue"

        newImmunization = LabelFrame(theFrame,bg="light blue",width=canvasWidth - 10,height=150,
                                     highlightcolor="white",highlightthickness=2,bd=0)
        newImmunization.place(x=5, y=startingY)


        immunizationName = "ImmunizationName: " + immunizationName

        administeredString = "Adminstered: "
        administeredString = datesAdministered

        administeredString = administeredString.rstrip(", ")

        immunizationLabel = Label(newImmunization,text=immunizationName,font=generalFont,bg=generalBG)
        immunizationLabel.place(x=5,y=0)
        immunizationLabel.update()

        nextY = immunizationLabel.winfo_y() + immunizationLabel.winfo_height() + 15

        administeredLabel = Label(newImmunization,text=administeredString,font=generalFont,bg=generalBG)
        administeredLabel.place(x=5,y=nextY)
        administeredLabel.update()

        nextY = administeredLabel.winfo_height() + administeredLabel.winfo_y() + 30


        learnMoreButton = Button(newImmunization, text="Learn more", font=generalFont,command=lambda: self.openWebPage(url))
        learnMoreButton.place(x=5,y=nextY)


        return newImmunization # return the Frame holding all this



    def showDemos(self): # secondary attempt at the demos page

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
        patientDetailsList = ["Last Name","First Name","Nickname","Middle Initial","Prefix","Sex"]

        PatientDemographicsList = ["Last Name","First Name","Nickname","Middle Initial","Prefix","Sex",
                                   "D.O.B","Age", "Race", "Ethnicity","Pref. Language", "Deceased Status"]

        staticDetails = self.demoGraphics.demographics
        self.checkNone(staticDetails)

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
            newTextBox.place(x=160 + detailsPosXIncrease,y=detailsPosY)
            newTextBox.insert('end',str(staticDetails[index]))
            newTextBox.configure(state=DISABLED)

            detailsPosY += 30


        self.addressFrame = LabelFrame(self.demosPage,text="Patient Address Details",width=Width-10,height=100,bg="light blue",
                                       highlightcolor="white",highlightthickness=2,font=('consolas',12),bd=0,labelanchor="n")

        self.addressFrame.place(x=5,y=self.patientFrame.winfo_y() + self.patientFrame.winfo_height() + 5)
        self.addressFrame.update()

        addressLabels = ["Street 1", "Street 2", "City ", "State", "Zipcode", "County ", "Country"]
        staticAddress = self.demoGraphics.address
        self.checkNone(staticAddress)

        addedLabels = []

        for label in addressLabels:
            newLabel = Label(self.addressFrame, text= label, bg="light blue", font=('consolas', 12))
            newLabel.update()
            addedLabels.append(newLabel)


        addedLabels[0].place(x=5,y=5)

        addedLabels[1].place(x=5,y=35)

        addedLabels[2].place(x=260,y=5)

        addedLabels[3].place(x=260,y=35)

        addedLabels[4].place(x=490,y=5)

        addedLabels[5].place(x=490,y=35)

        addedLabels[6].configure(font=('consolas', 12))
        addedLabels[6].place(x=740,y=3)

        yPos = 5
        for index in range(len(staticAddress)):

            if index == 6:
                #currentLabel = addedLabels[index]
                addedLabels[index].update()
                yPos = addedLabels[index].winfo_height() + 10
                xPos = addedLabels[index].winfo_x()

                addedText = staticAddress[index]

                newText = Text(self.addressFrame, width=8,
                               height=1)  # Replaced dynamic width=len(addedText) with fixed size
                newText.place(x=xPos, y=yPos)
                newText.insert('end', addedText)
                newText.configure(state=DISABLED)

                break

            if yPos > 35:
                yPos = 5

            addedLabels[index].update()
            xPos = addedLabels[index].winfo_x() + addedLabels[index].winfo_width() + 1


            addedText = staticAddress[index]

            addedText = str(addedText)
            newText = Text(self.addressFrame,width=len(addedText),height=1)
            newText = Text(self.addressFrame,width=18,height=1)#Replaced dynamic width=len(addedText) with fixed size
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
        self.demosNoteBook.add(self.demoOtherFrame, text=" Insurance ")

        #contact information displayed below here

        contactLabels = ["Home Number  ","Mobile Number","Work Number  ", "Ext", "Email Address", "Preferred Mode of Contact",
                         "Interpreter Required"]

        staticContactINFO = self.demoGraphics.contact
        self.checkNone(staticContactINFO)


        xPos = 5
        yPos = 5
        ExtXPos = 0

        self.contactINFO.update()
        for index in range(len(contactLabels)):

            labelInsert = contactLabels[index]
            textInsert = staticContactINFO[index]

            widgetlength = 17


            newLabel = Label(self.contactINFO,text=labelInsert,font=('consolas',12),bg="light blue")

            if labelInsert == "Ext":
                widgetlength = 10
                newLabel.place(x=ExtXPos, y=yPos)
                newLabel.update()
            else:
                newLabel.place(x=xPos, y=yPos)
                newLabel.update()


            textX = newLabel.winfo_width() + newLabel.winfo_x() + 5
            textY = newLabel.winfo_y()

            if len(textInsert) > widgetlength:
                newText = Text(self.contactINFO, width=35, height=1,
                               font=('consolas', 12))  # changed dynamic width=len(textInsert) to fixed number.
                newText.insert('end', textInsert)
                newText.configure(state=DISABLED)
                newText.place(x=textX, y=textY)
                newText.update()
            else:
                newText = Text(self.contactINFO,width=widgetlength,height = 1,font=('consolas',12)) #changed dynamic width=len(textInsert) to fixed number.
                newText.insert('end',textInsert)
                newText.configure(state=DISABLED)
                newText.place(x=textX,y=textY)
                newText.update()

            if labelInsert == "Work Number  ":
                ExtXPos = newText.winfo_x() + newText.winfo_width() + 10
            else:
                yPos += 45



        contactNotesLabel = Label(self.contactINFO,text="Contact Notes",bg="light blue",font=('consolas',12))
        contactNotesLabel.place(x=550,y=5)
        contactNotesLabel.update()

        '''formattedString = ''
        print(self.ContactNotes)
        for newline in self.ContactNotes:
            formattedString += str(newline)'''

        contactNotesText = Text(self.contactINFO,width=35,height=12,padx=5)
        #contactNotesText.configure(state=DISABLED)
        contactNotesText.place(x=460,y=contactNotesLabel.winfo_y() + contactNotesLabel.winfo_height() + 5)
        #contactNotesText.insert('end', formattedString)
        contactNotesText.insert('end', str(self.ContactNotes[0][0]))
        contactNotesText.configure(state=DISABLED)
        contactNotesText.update()

        updateButtonX = contactNotesLabel.winfo_x()
        updateButtonY = contactNotesText.winfo_y() + contactNotesText.winfo_height() + 5

        updateButton = Button(self.contactINFO, text = "Update Contact Notes", font=('consolas' ,10), command=lambda : self.updateContactNotes(contactNotesText.get("1.0",END), self.thisPatient.patientID))
        updateButton.place(x=updateButtonX, y=updateButtonY)


        #guarantor information

        guarantorInformationlabels = ["First Name", "Last Name","Middle Initial", "GuarantorGender"]

        #####This section populates the 'other' tab in the patient details#####

        #headerLabel = Label(self.demoOtherFrame,text="These are just here for testing purposes")
        #headerLabel.pack()

        #guarantorButton = Button(self.demoOtherFrame,text="Guarantor Extension before update",command=self.extensionGuarantor)
        #guarantorButton.pack()


        #emailButton = Button(self.demoOtherFrame,text="Email Extension before update",command=self.extensionEmail)
        #emailButton.pack()

        self.extensionGuarantor()
        self.extensionInsurance()

    def extensionGuarantor(self): # display the Guarantor in the extension

        self.guarantorInformation.update()
        width = self.guarantorInformation.winfo_width()
        height = 300

        #self.addExtension()


        #obtain information here


        generalFont = ('consolas',12) # general font used for the labels

        #newText = Text(self.contactINFO, width=len(textInsert), height=1, font=('consolas', 12))


        # extension title
        #testLabel = Label(self.guarantorInformation,text="Guarantor Information",relief=GROOVE, font=('consolas',19))
        #testLabel.place(x=0,y=0)

        informationLabel = ["First name", "Last Name ", "Middle Initial", "Sex  ", "Relationship to Patient", "Home Phone   ", "Mobile Number"]

        staticInfo = self.demoGraphics.guarantor
        self.checkNone(staticInfo)


        self.guarantorLabels = {} # contains labels that are connected to label text/ginfo

        xPos = 5
        yPos = 10
        for index in range(len(informationLabel)): # set the page up

            formatText = informationLabel[index] # guarantor labels
            ourText = staticInfo[index] # database values

            newLabel = Label(self.guarantorInformation, text=formatText, font=generalFont, bg='light blue')
            newLabel.place(x=xPos, y=yPos)

            newLabel.update()

            formatWidth = newLabel.winfo_width() + 15 + newLabel.winfo_x()

            gINFO = Text(self.guarantorInformation,width = 20, height = 1, font = generalFont) #replacing dynamic width = len(ourText) with fixed width
            gINFO.insert("end", ourText)
            gINFO.configure(state=DISABLED)
            gINFO.place(x=formatWidth,y=yPos)

            yPos += 50

            self.guarantorLabels[formatText] = newLabel # store our labels connected to the formattedText
            if yPos >= height-100:
                xPos += 350
                yPos = 5

        #closeButton = Button(self.extensionFrame,text = "Close Guarantor Example Page", command= self.removeExtension)
        #closeButton.place(x=50,y=450)

    def extensionInsurance(self):  # display the InsuranceTab in the extension

        self.demoOtherFrame.update()
        width = self.demoOtherFrame.winfo_width()
        height = 300

        # obtain information here

        generalFont = ('consolas', 12)  # general font used for the labels

        insuranceTabLabels = ["Provider First Name", "Last Visit Date    ", "Insurance Active   ", "Insurance Name     ", "Provider Last Name",
                                "Provider NPI      "]

        staticInsuranceInfo = self.InsuranceTab
        self.checkNone(staticInsuranceInfo)

        self.insuranceLabels = {}  # contains labels that are connected to label text/ginfo

        xPos = 5
        yPos = 10
        for index in range(len(insuranceTabLabels)):  # set the page up

            formatText = insuranceTabLabels[index]  # guarantor labels
            ourText = staticInsuranceInfo[0][index]  # database values

            newLabel = Label(self.demoOtherFrame, text=formatText, font=generalFont, bg='light blue')
            newLabel.place(x=xPos, y=yPos)

            newLabel.update()

            formatWidth = newLabel.winfo_width() + 15 + newLabel.winfo_x()

            InsTabINFO = Text(self.demoOtherFrame, width=20, height=1,
                             font=generalFont)  # replacing dynamic width = len(ourText) with fixed width
            InsTabINFO.insert("end", ourText)
            InsTabINFO.configure(state=DISABLED)
            InsTabINFO.place(x=formatWidth, y=yPos)

            yPos += 50

            self.insuranceLabels[formatText] = newLabel  # store our labels connected to the formattedText
            if yPos >= height - 100:
                xPos += 400
                yPos = 5

    def label_and_Text(self,frame,labelText,labelRow,labelCol,boxText):

        lNameLabel = Label(frame, text='{0:<10}'.format(labelText),font=('consolas',11),bg="light blue")
        lNameLabel.grid(row=labelRow, column=labelCol,padx=10)

        patientLname = Text(frame, width=len(boxText), height=1,padx=5,font=('consolas',11))
        patientLname.insert('end', boxText)
        patientLname.configure(state=DISABLED)
        patientLname.grid(row=labelRow+2, column=labelCol)

    def putFormat(self):

        formatString = '{0:<20}{1:<35}{2:<20}{3:<15}'.format("Service ID", "Immunization",
                                                                   "Administered", "Service Date")

        self.formatLabel = Label(self.servicePage, text=formatString, font=('Consolas', 11)
                            , relief="raised",width=900,height=2)
        self.formatLabel.pack()
        self.formatLabel.update()

    def showService(self): # uses servicePage Canvas for display

        self.putFormat()

        self.newFrame = Frame(self.servicePage, relief=GROOVE, bd=1)
        self.newFrame.place(x=0, width=848, y=40, height=660)

        self.canvas = Canvas(self.newFrame,bg="light blue")
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
        SQL = self.SQL
        serviceHistory = SQL.getServiceDetails(self.thisPatient.patientID)



        if not self.myScrollBar.winfo_ismapped():  # will repack scroll bar and formatLabel
            self.formatLabel.forget()
            self.putFormat()
            self.formatLabel.pack()
            self.myScrollBar.pack(side="right", fill="y")



        for index in range(len(serviceHistory)): # This is where we would queue the database for information. Probably modify to only do once
            # print((serviceHistory.ServiceDetailsId))
            serviceID = str(serviceHistory.ServiceDetailsId[index])


            patientINFO = [serviceID, \
                           serviceHistory.ImmDisplayDescription[index], \
                           serviceHistory.CompletionStatus[index], \
                           serviceHistory.DateofService[index],\
                           serviceHistory.AllergicReactions[index],
                           serviceHistory.ProviderLastName[index],
                           serviceHistory.ProviderFirstName[index],
                           serviceHistory.InformationSource[index]]
            buttonINFO = self.formatService(patientINFO)

            self.serviceHistory = [] # holds all service
            button = Button(self.newnewFrame, text = buttonINFO,anchor=W,justify=LEFT, width = 102, font=('Consolas', 11))
            button.grid(row=index)
            button.configure(command=lambda x=patientINFO: self.loadService(x))
            self.serviceHistory.append(button)


    def formatService(self,patientService): # will format the buttons to be displayed in the service history

        #{0: < 20}{1: < 35}{2: < 20}{3: < 15}

        if len(patientService[1]) > 30:
            immunizationString = patientService[1][0:30] + ".."
        else:
            immunizationString = patientService[1]

        formatString = '{0:<9}{1:<13}{2:<40}{3:<20}{4:<15}'.format("",patientService[0],immunizationString,patientService[2],patientService[3])

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
        patientService = [serviceID,immunizations[1], compliance[0],ServiceDate]

        self.formatService(patientService)



    def loadService(self,patientINFO): # will display specific service in expansion window

        #does basic setup for the service screen
        self.hideServiceHistory()

        # resets the header
        self.formatLabel.destroy()
        self.formatLabel = Label(self.servicePage,text="Showing details for Service #" + patientINFO[0],font=('Consolas', 11)
              , relief="raised", width=800, height=2)
        self.formatLabel.pack()

        self.myScrollBar.pack_forget()
        self.canvas.yview_moveto(0)


        #general widget settings
        generalFont = ('consolas', 12)
        generalBG = "light blue"
        theFrame = self.newnewFrame
        theFrame.configure(width=850,height=700)



        #static data that is used during developement
        DOS = patientINFO[3]
        receivedImmunization = patientINFO[1]
        #print(receivedImmunization)
        immunizationABBV = "DTaP"
        allergicReactions = patientINFO[4]
        print(allergicReactions)

        xPos = 150
        yPos = 10
        increment = 20
        textX = 300

        serviceDetailsHeader = Label(theFrame,text="Service Details",width= theFrame.winfo_width(),height = 1,bg="RoyalBlue3",font=generalFont,fg="white",anchor=W)
        serviceDetailsHeader.place(x=0,y=0)
        serviceDetailsHeader
        serviceDetailsHeader.update()

        serviceFrame = LabelFrame(theFrame,text = "Service Details",width=830,height=610,bg="light blue",
                                       highlightcolor="white",highlightthickness=2,font=('consolas',12),bd=0,labelanchor="n")
        serviceFrame.place(x=5,y=5)
        serviceFrame.update()

        yPos = serviceDetailsHeader.winfo_height() + serviceDetailsHeader.winfo_y() + increment

        serviceDateLabel = Label(serviceFrame,text="Date of Service",bg=generalBG,font=generalFont)
        serviceDateLabel.place(x=xPos,y=yPos)
        serviceDateLabel.update()

        serviceDateText = Text(serviceFrame,width=len(DOS),height = 1,font=generalFont)
        serviceDateText.place(x=textX,y=yPos)
        serviceDateText.insert('end',DOS)
        serviceDateText.configure(state=DISABLED)

        yPos = serviceDateLabel.winfo_height() + serviceDateLabel.winfo_y() + increment


        immunizationLabel = Label(serviceFrame,text="Immunizations Received",bg=generalBG,font=generalFont)
        immunizationLabel.place(x=xPos,y=yPos)
        immunizationLabel.winfo_toplevel()
        immunizationLabel.update()


        immuX = immunizationLabel.winfo_width() + immunizationLabel.winfo_x()



        # place the immunizations received into this list
        immuReceived = receivedImmunization


        immunizationsReceived = Text(theFrame, width=len(immuReceived),font=generalFont, height=1 )
        #immunizationsReceived.set(immuReceived[0]) # is set to the first value of the list
        immunizationsReceived.insert('end',immuReceived)
        immunizationsReceived.place(x=immuX,y=yPos)
        immunizationsReceived.configure(state=DISABLED)
        immunizationsReceived.update()



        immuXtension = immunizationsReceived.winfo_width() + immunizationsReceived.winfo_x() + 10
        extendImmunizationButton = Button(serviceFrame,text="Information on \nSelected Immunization",
                                        command= lambda : self.immunizationINFO(immunizationsReceived.get()))
        extendImmunizationButton.place(x=immuXtension-150,y=yPos+40)


        yPos = immunizationLabel.winfo_y() + immunizationLabel.winfo_height() + increment


        completionStatusLabel = Label(serviceFrame,text="Completion Status",bg=generalBG,font=generalFont)
        completionStatusLabel.place(x=xPos,y=yPos)
        completionStatusLabel.update()


        completionX = completionStatusLabel.winfo_x() + completionStatusLabel.winfo_width() + 5

        completionStatusText = Text(theFrame,width=len(patientINFO[2]),font=generalFont,height=1)

        completionStatusText.place(x=completionX,y=yPos)
        completionStatusText.insert('end',(patientINFO[2]))
        completionStatusText.configure(state=DISABLED)


        yPos = completionStatusLabel.winfo_y() + completionStatusLabel.winfo_height() + increment


        informationSourceLabel = Label(serviceFrame,text="Information Source",bg=generalBG,font=generalFont)
        informationSourceLabel.place(x=xPos,y=yPos)
        informationSourceLabel.update()

        informationX = informationSourceLabel.winfo_width() + informationSourceLabel.winfo_x() + 5

        informationSourceText = Text(serviceFrame,width=15,font=generalFont,height=1)
        informationSourceText.place(x=informationX,y=yPos)
        #print(patientINFO[7])
        informationSourceText.insert('end', patientINFO[7])
        informationSourceText.configure(state=DISABLED)


        yPos = informationSourceLabel.winfo_y() + informationSourceLabel.winfo_height() + increment

        sourceSystemLabel = Label(serviceFrame,text="Source System",bg=generalBG,font=generalFont)
        sourceSystemLabel.place(x=xPos,y=yPos)
        sourceSystemLabel.update()

        sourceX = sourceSystemLabel.winfo_x() + sourceSystemLabel.winfo_width() + 5


        sourceSystemText = Text(serviceFrame,width=15,font=generalFont,height=1)
        sourceSystemText.place(x=sourceX,y=yPos)
        sourceSystemText.insert('end','EMR')
        sourceSystemText.configure(state=DISABLED)




        yPos = sourceSystemLabel.winfo_y() + sourceSystemLabel.winfo_height() + increment

        '''
        reactionsHeader = Label(serviceFrame, text="Reactions", width=theFrame.winfo_width(), height=1,
                                     bg="RoyalBlue3", font=generalFont, fg="white", anchor=W)

        reactionsHeader.place(x=0,y=yPos + 30)
        reactionsHeader.update()
    
        yPos = reactionsHeader.winfo_height() + reactionsHeader.winfo_y() + increment
        '''


        allergicReactionsLabel = Label(serviceFrame,text="Allergic Reactions",bg=generalBG,font=generalFont)
        allergicReactionsLabel.place(x=xPos,y=yPos)
        allergicReactionsLabel.update()



        allergicReactionsText = Text(theFrame,width=30,height=3)
        allergicReactionsText.place(x=textX+30,y=yPos)
        allergicReactionsText.insert('end', allergicReactions)
        allergicReactionsText.configure(state=DISABLED)
        allergicReactionsText.update()

        yPos = allergicReactionsText.winfo_y() + allergicReactionsText.winfo_height() + increment

        '''
        serviceProviderHeader = Label(serviceFrame,text="Service Provider",bg="RoyalBlue3",fg="white",
                                      font=generalFont,anchor=W,
                                      width=theFrame.winfo_width(),height=1)
        serviceProviderHeader.place(x=0,y=yPos)
        serviceProviderHeader.update()


        yPos = serviceProviderHeader.winfo_height() + serviceProviderHeader.winfo_y() + increment
        '''


        serviceProviderLabel = Label(serviceFrame,text="Provider Name",bg=generalBG,font=generalFont)
        serviceProviderLabel.place(x=xPos,y=yPos)
        serviceDateLabel.update()

        providerX = serviceDateLabel.winfo_x() + serviceDateLabel.winfo_width() + 10


        serviceProviderText = Text(serviceFrame,width=20,height=1,font=generalFont)
        serviceProviderText.place(x=providerX,y=yPos)
        providerName = patientINFO[5]+', '+patientINFO[6]
        serviceProviderText.insert('end',providerName)
        serviceProviderText.configure(state=DISABLED)
        serviceProviderText.update()

        yPos += (serviceProviderText.winfo_height() + increment + 25)


        returnButton = Button(serviceFrame,text="Back to Service History",bg="RoyalBlue3",fg="white",font=generalFont,
                              command=self.displayServiceHistory)
        returnButton.place(x=xPos,y=yPos)

    def immunizationINFO(self,immunization): # will display the webpage for the immunization

        # kinda brute force but it works
        immunization = immunization.strip("{")
        immunization = immunization.strip("}")

        try:
            url = self.switchURL[immunization]
            self.openWebPage(url)

        except KeyError:
            messagebox.showerror("Error 404", "The select immunization\nwas not found...")
            print(immunization + "was not found in our information sources")



    def extensionImmunization(self): # pass detailed immunization information here and place on extension window

        self.addExtension()
        self.checkExtension()
        theFrame = self.extensionFrame # easier to reference
        generalFont = ('consolas', 12)

        immunizationName = "DTaP (Diphtheria, Tetanus, acellular Pertussis)"
        immunizationName2 = "HBV (Hepatitis B)"


        immunizationHeader = Label(theFrame,text=immunizationName,font=generalFont,wraplengt=300)
        immunizationHeader.place(x=50,y=0)


    def showOutReach(self): # newer version of outreaching to patients

        # Setup for  the contact page
        self.contactPage.update()
        Width = 850

        self.contactPage.configure(bg="light blue")
        generalBG = "light blue"
        generalFont = ('consolas',14)


        # initialized vars
        theFrame = self.contactPage

        contactFrame = LabelFrame(theFrame,bg="light blue",width=Width-10,height=150,
                                            highlightcolor="white",highlightthickness=2,bd=0)
        contactFrame.place(x=5,y=5)

        labels = ["Home Phone","Mobile Phone","Preferred Contact","Interpreter",
                  "Guarantor Name","Guarantor Relationship"]

        # Queue for textboxes here
        if(self.OutreachDetails is None):
            self.outreachDetails=[None,None,None,None,None,None,None,None]
        self.checkNone(self.OutreachDetails)
        staticInformation = self.OutreachDetails[0][:2]
        staticInformation.extend(self.OutreachDetails[0][4:8])
        self.checkNone(staticInformation)
        patientLabels = []
        patientText = []
        self.outreachWidgets = []

        for index in range(len(labels)):

            insertText = staticInformation[index]

            if insertText == None:
                insertText = ""

            #create new label for the frame
            newLabel = Label(contactFrame,text = labels[index],bg="light blue", font = ('consolas',12))

            newText = Text(contactFrame,width=20,height=1)
            #print(staticInformation[index])
            newText.insert('end',staticInformation[index])
            newText.configure(state=DISABLED)

            patientLabels.append(newLabel)
            patientText.append(newText)


        index = 0
        startingX = 5
        startingY = 5
        labelPTR = None


        # will refactor into a for loop later
        patientLabels[index].place(x=startingX,y=startingY)
        patientLabels[index].update()
        nextX = patientLabels[index].winfo_x() + patientLabels[index].winfo_width() + 3

        patientText[index].place(x=nextX,y=startingY)
        startingY = patientLabels[index].winfo_y() + patientLabels[index].winfo_height() + 20
        index += 1


        patientLabels[index].place(x=startingX, y=startingY)
        patientLabels[index].update()
        nextX = patientLabels[index].winfo_x() + patientLabels[index].winfo_width() + 3

        patientText[index].place(x=nextX, y=startingY)
        startingY = patientLabels[index].winfo_y() + patientLabels[index].winfo_height() + 20
        index += 1

        patientLabels[index].place(x=startingX, y=startingY)
        patientLabels[index].update()
        nextX = patientLabels[index].winfo_x() + patientLabels[index].winfo_width() + 10

        patientText[index].place(x=nextX, y=startingY)
        startingY = 5
        startingX = 400
        index += 1

        patientLabels[index].place(x=startingX, y=startingY)
        patientLabels[index].update()
        nextX = patientLabels[index].winfo_x() + patientLabels[index].winfo_width() + 10

        patientText[index].place(x=nextX, y=startingY)
        startingY = patientLabels[index].winfo_y() + patientLabels[index].winfo_height() + 20
        index += 1

        patientLabels[index].place(x=startingX, y=startingY)
        patientLabels[index].update()
        nextX = patientLabels[index].winfo_x() + patientLabels[index].winfo_width() + 10

        patientText[index].place(x=nextX, y=startingY)
        startingY = patientLabels[index].winfo_y() + patientLabels[index].winfo_height() + 20
        index += 1



        patientLabels[index].place(x=startingX, y=startingY)
        patientLabels[index].update()
        nextX = patientLabels[index].winfo_x() + patientLabels[index].winfo_width() + 10

        patientText[index].place(x=nextX, y=startingY)
        startingY = 45
        startingX = 475
        index += 1

        '''patientLabels[index].place(x=startingX, y=startingY)
        patientLabels[index].update()
        nextX = patientLabels[index].winfo_x() + patientLabels[index].winfo_width() + 10

        patientText[index].place(x=nextX, y=startingY)
        startingY = patientLabels[index].winfo_y() + patientLabels[index].winfo_height() + 20
        index += 1

        patientLabels[index].place(x=startingX, y=startingY)
        patientLabels[index].update()
        nextX = patientLabels[index].winfo_x() + patientLabels[index].winfo_width() + 10

        patientText[index].place(x=nextX, y=startingY)
        startingY = patientLabels[index].winfo_y() + patientLabels[index].winfo_height() + 20
        index += 1'''

        contactFrame.update()
        nextFrameY = contactFrame.winfo_y() + contactFrame.winfo_height() + 5


        # label frame for outreach details

        self.outreachDetailsFrame = LabelFrame(theFrame, text="Outreach Details", width=Width - 10, height=250,
                                       bg="light blue",
                                       highlightcolor="white", highlightthickness=2, font=('consolas', 12), bd=0,
                                       labelanchor="n")
        self.outreachDetailsFrame.place(x=5,y=nextFrameY)
        self.outreachDetailsFrame.update()

        Width = self.outreachDetailsFrame.winfo_width()
        Height = self.outreachDetailsFrame.winfo_height()

        detailsLabels = ["Date", "Method", "Outcome","Attempt Number"]


        outcomeLabels = ["Answered", "Missed Call", "Hung Up","Will Call Back","Wrong Number", "Attempt Again Later","Awaiting response"]
        methodLabels = ["Email", "Phone", "Letter"]
        outComeBox = Combobox(self.outreachDetailsFrame, values=outcomeLabels)
        methodBox = Combobox(self.outreachDetailsFrame,values=methodLabels)


        xPos = 5
        yPos = 5
        for label in detailsLabels:

            newLabel = Label(self.outreachDetailsFrame,text=label,font=generalFont,bg=generalBG)
            newLabel.place(x=xPos,y=yPos)
            newLabel.update()
            xPos = newLabel.winfo_x() + newLabel.winfo_width() + 15

            outReachAttempt = self.SQL.getOutReachAttempt(self.thisPatient.patientID)
            if label != "Outcome" and label != "Method":

                if label == "Date":
                    today = date.today()
                    newText = Text(self.outreachDetailsFrame, width=20, height=1)
                    newText.place(x=xPos, y=yPos)
                    newText.insert('end',today)
                    newText.configure(state=DISABLED)
                    newText.update()
                    self.outreachWidgets.append(newText)
                    yPos = newLabel.winfo_height() + newLabel.winfo_y()

                elif label == "Attempt Number":
                    newText = Text(self.outreachDetailsFrame, width=20, height=1)
                    newText.place(x=xPos, y=yPos)
                    newText.insert('end', str(outReachAttempt))
                    newText.configure(state=DISABLED)
                    newText.update()
                    self.outreachWidgets.append(newText)
                    yPos = newLabel.winfo_height() + newLabel.winfo_y()
                else:
                    newText = Text(self.outreachDetailsFrame,width = 20,height=1)
                    newText.place(x=xPos,y=yPos)
                    newText.update()
                    self.outreachWidgets.append(newText)

                    yPos = newLabel.winfo_height() + newLabel.winfo_y()

            elif label == "Outcome":
                outComeBox.place(x=xPos,y=yPos)
                outComeBox.update()
                self.outreachWidgets.append(outComeBox)
                yPos = newLabel.winfo_height() + newLabel.winfo_y()

            elif label == "Method":
                methodBox.place(x=xPos,y=yPos)
                methodBox.update()
                self.outreachWidgets.append(methodBox)
                yPos = newLabel.winfo_height() + newLabel.winfo_y()

            xPos = 5


        outReachNotesLabel = Label(self.outreachDetailsFrame,text = "Outreach Notes",bg=generalBG,font=generalFont)
        outReachNotesLabel.place(x=550,y=0)
        outReachNotesLabel.update()


        outReachNotesX = outReachNotesLabel.winfo_x()
        outReachNotesY = outReachNotesLabel.winfo_y() + 8

        outReachNotesText = Text(self.outreachDetailsFrame,width=32,height=8)
        outReachNotesText.place(x=outReachNotesX-50,y=outReachNotesY)
        outReachNotesText.update()
        self.outreachWidgets.append(outReachNotesText)


        previousAttemptsX = outReachNotesText.winfo_x()
        previousAttemptsY = 180

        previousAttempts = Button(self.outreachDetailsFrame,text="Previous Attempts",font=('consolas',10),command=self.showAttempts)
        previousAttempts.place(x=previousAttemptsX,y=previousAttemptsY)
        previousAttempts.update()
        self.outreachDetailsFrame.update()

        nextY = self.outreachDetailsFrame.winfo_y() + self.outreachDetailsFrame.winfo_height() + 5
        nextX = previousAttempts.winfo_x() + previousAttempts.winfo_width() + 15


        updateButton = Button(self.outreachDetailsFrame, text="Submit Outreach", font=('consolas', 10),
                              command=self.appendOutreach)
        updateButton.place(x=nextX, y=previousAttemptsY)



        # self.demosPage,width = Width - 25, height = Height - self.patientFrame.winfo_height() - self.addressFrame.winfo_height(),padding = 5
        self.outreachNotebook = ttk.Notebook(theFrame, width=Width-10, height=Height-nextY,padding = 5)
        self.emailFrame = Frame(self.outreachNotebook,width=775,height=300,bg="light blue")
        self.outreachNotebook.add(self.emailFrame, text="Email Patient")
        self.outreachNotebook.place(x=5,y=nextY)

        emailFrame = self.emailFrame # pointer to easily reference the frame

        sendEmailLabel = Label(emailFrame,text = "Sending email to: " + self.patientFULL, font=generalFont,bg=generalBG)
        sendEmailLabel.place(x=5,y=5)
        sendEmailLabel.update()
    
        emailY = sendEmailLabel.winfo_y() + sendEmailLabel.winfo_height() + 5

        self.emailText = Text(emailFrame,width = 50,height=10)
        self.emailText.place(x=5,y=emailY)

        startingY = 30

        buttonFrame = LabelFrame(emailFrame,text="Email Options",width=335,height=200,bg="light blue",
                                       highlightcolor="white",highlightthickness=2,font=('consolas',12),bd=0,labelanchor="n")
        buttonFrame.place(x=480,y=20)
        buttonFrame.update()

        middleX = (buttonFrame.winfo_width() / 2) - 100


        template1 = Button(buttonFrame, text="Load\n Template 1", command=lambda: self.loadTemplate(1))
        template1.place(x=middleX, y=startingY)
        template1.update()

        nextX = template1.winfo_width() + template1.winfo_x() + 50

        template2 = Button(buttonFrame, text="Load\n Template 2", command=lambda: self.loadTemplate(2))
        template2.place(x=nextX, y=startingY)

        sendEmail = Button(buttonFrame, text="Send Email!", command=self.sendEmail)
        sendEmail.place(x=middleX, y=startingY + 75)

        clearEmail = Button(buttonFrame, text="Clear Email", command=self.clearEmailEntry)
        clearEmail.place(x=nextX, y=startingY + 75)

    def showOutreachAttempt(self,thisAttempt = None):

        for widget in self.outreachDetailsFrame.winfo_children():
            widget.destroy() # clear the attempt buttons


        attemptNumber = 1 # would get the attempt number from the list information
        self.outreachDetailsFrame.configure(text="Attempt #" + str(attemptNumber))

        if thisAttempt == None:
            thisAttempt = ["","","","",""] # empty spots to hold the strings

        generalBG = "light blue"
        generalFont = ('consolas', 14)
        detailsLabels = ["Date", "Method", "Outcome", "Attempt Number"]

        xPos = 5
        yPos = 5
        currentIndex = 0
        for index in range(len(detailsLabels)):

            newLabel = Label(self.outreachDetailsFrame, text=detailsLabels[index], font=generalFont, bg=generalBG)
            newLabel.place(x=xPos, y=yPos)
            newLabel.update()
            xPos = newLabel.winfo_x() + newLabel.winfo_width() + 15


            newText = Text(self.outreachDetailsFrame, width=20, height=1)
            newText.place(x=xPos, y=yPos)
            newText.insert(END,thisAttempt[index])
            newText.configure(state=DISABLED)
            newText.update()
            self.outreachWidgets.append(newText)
            yPos = newLabel.winfo_height() + newLabel.winfo_y()
            xPos = 5
            currentIndex = index

        outReachNotesLabel = Label(self.outreachDetailsFrame, text="Outreach Notes", bg=generalBG, font=generalFont)
        outReachNotesLabel.place(x=550, y=0)
        outReachNotesLabel.update()

        outReachNotesX = outReachNotesLabel.winfo_x()
        outReachNotesY = outReachNotesLabel.winfo_y() + 8

        outReachNotesText = Text(self.outreachDetailsFrame, width=32, height=8)
        outReachNotesText.insert(END,thisAttempt[currentIndex])
        outReachNotesText.configure(state=DISABLED)
        outReachNotesText.place(x=outReachNotesX - 50, y=outReachNotesY)
        outReachNotesText.update()

        goBackButton = Button(self.outreachDetailsFrame, text="Create New Attempt", command=self.resetOutReachPage)
        goBackButton.place(x=600, y=185)

    def appendOutreach(self):
        '''
        Widgets are placed in order of:
        Date, Method, Outcome, Attempt Number, Outreach Notes
        These are all text widgets so getting info from them is just using the .get() function
        '''

        newList = []

        for widget in self.outreachWidgets: # will retrieve all data and put into new list

            if type(widget) == type(Text()):

                currentString = widget.get("1.0",END)
                print(currentString)
                newList.append(currentString) # obtains all the text from widget
            else:
                currentString = widget.get()
                newList.append(currentString)

        outreachList = [self.user.userId, "OutreachDetails", newList[1], newList[2], newList[4], self.thisPatient.patientID]
        self.SQL.addOutreach(outreachList)
        # script to update database goes here
        # newList will contain all the information to append

    def showAttempts(self):

        generalFont = ('consolas', 14)
        xPos = 400
        yPos = 25
        for widget in self.outreachDetailsFrame.winfo_children():
            widget.destroy()

        self.outreachDetailsFrame.configure(text="Previous Attempts")

        # this would be the queue from the database
        attempts = [["","","","","",""]] # this would be a 2D array of info that can be populated back into the frame


        attemptIndex = 0 # temp for now to show index
        for attempt in attempts:
            newButton = Button(self.outreachDetailsFrame,text="Attempt#" + str(attemptIndex),font=generalFont,
                               command=lambda : self.showOutreachAttempt(attempt))
            newButton.place(x=xPos,y=yPos)
            yPos += 50


        goBackButton = Button(self.outreachDetailsFrame,text="Go Back",command=self.resetOutReachPage)
        goBackButton.place(x=700,y=600)


    def resetOutReachPage(self):

        for widget in self.contactPage.winfo_children():
            widget.destroy() # clears the entire outreach page

        self.showOutReach() # re populate the entire page


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

    def checkNone(self,myList): # checks if any of the information being added is of None type

        for index in range(len(myList)):

            if myList[index] == None:
                myList[index] = ""


    def addImmunizationLink(self,immunizationName,url): # append an immunization along with the link to the dictionary

        self.switchURL[immunizationName] = url

    def generateImmunizationLinks(self): # Default immunization names/ corresponding links are placed here


        #We could also populate the referenced links in the database if we wanted as well



        self.switchURL = { # immunization names and corresponding links are placed in here
            "Why is it important to get annual flu vaccine?": "https://www.cdc.gov/flu/prevent/keyfacts.htm",
            "What are the benefits of flu vaccination?": "https://www.cdc.gov/flu/prevent/vaccine-benefits.htm",
            "Influenza Vaccine FluMistQuadrivalent": "https://www.cdc.gov/vaccines/hcp/vis/vis-statements/flulive.html"
        }

        influenzaPrevFreeInformation = ["Influenza Vaccine Prev Free 0.25 ml",
                                        "Influenza Vaccine Prev Free 0.5 ml",
                                        "Influenza Vaccine ccIIV4 Prev Free 0.5 ml"]

        for newInfo in influenzaPrevFreeInformation:  # adds the Prev free immunization plus their links to the page
            self.switchURL[newInfo] = "https://www.verywellhealth.com/preservative-free-flu-vaccine-770551"

        influenzaInformation = ["Influenza Vaccine quad split virus 0.5 ml",
                                "Influenza Vaccine quad split virus Prev Free ID Use",
                                "Influenza Vaccine quad split virus Prev Free 0.25 ml",
                                "Influenza Vaccine quad split virus Prev Free 0.5 ml"]

        for newInfo in influenzaInformation:  # adds the immunization info for the next batch of immunizations we are storing
            self.switchURL[newInfo] = "https://www.cdc.gov/flu/prevent/quadrivalent.htm"

        influenzaInformation = ['Influenza Vaccine RIV4']
        for newInfo in influenzaInformation:
            self.switchURL[newInfo] = 'https://www.cdc.gov/flu/prevent/qa_flublok-vaccine.htm'
        influenzaInformation = ['Influenza Vaccine FluMistQuadrivalent']
        for newInfo in influenzaInformation:
            self.switchURL[newInfo] = 'https://www.flumistquadrivalent.com/nasal-spray-flu-vaccine/how-does-it-work.html'
        influenzaInformation = ['Influenza Vaccine ccIIV4 0.5 ml']
        for newInfo in influenzaInformation:
            self.switchURL[newInfo] = 'https://www.cdc.gov/flu/professionals/acip/summary/summary-recommendations.htm#iivs'
        influenzaInformation = ["Influenza Vaccine 0.5 ml","Influenza Vaccine 0.25 ml"]
        for newInfo in influenzaInformation:
            self.switchURL[newInfo] = 'https://www.cdc.gov/flu/about/qa/vaxadmin.htm'


    def openWebPage(self,url): # will open the web browser from the buttom

        webbrowser.open(url,new=0,autoraise=True)

    def updateContactNotes(self, notes, pid):
        self.SQL.addContactNotes([notes, pid])
