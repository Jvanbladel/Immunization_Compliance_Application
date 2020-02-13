from icaScreens import *


class PatientScreen(icaSCREENS):
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
