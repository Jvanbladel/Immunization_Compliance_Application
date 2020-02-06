from tkinter import *
from tkinter import messagebox
import sqlite3

class icaSCREENS():
    '''
    Base class for all screens. Currently will only contain the root,
    clear the screen, and swap to other screens.
    '''
    screenSTACK = []
    def __init__(self,window): #all screens must contain the root window
        self.root = window

    def addTO(self): #add something new and its grid location
        print("Say")
    def remove(self,thisITEM): #remove this item from window.winfo.children
        print("Soon")

    def clearSCREEN(self):
        #will clear the screen of everything
        for widget in self.root.winfo_children():
            widget.destroy()

    def swapTO(self,newSCREEN): #pass the class of the screen you want to go to along with the window
        self.clearSCREEN()
        newSCREEN(self.root)

class mainMenu(icaSCREENS):

    def __init__(self,window):
        super().__init__(window)

        self.root.geometry("600x600")
        menu = Menu(self.root)

        labelFRAME = LabelFrame(self.root,text="User labels go here")
        labelFRAME.place(x=100,y=100,height=600,width=300)

        button = Button(self.root,text="Press me!",command=lambda: self.swapTO(med_INFO_SCREEN))
        button.place(x=0,y=0,height=200,width=100)

class med_INFO_SCREEN(icaSCREENS):
    '''
    Currently very basic. will have more features soon
    '''
    def __init__(self,window):
        super().__init__(window)
        self.dataBoxes = []

        titles = ["First Name", "Last Name", "Medical ID", "Last Outreach", "Last Immunization", "Provider"]
        defaultEntry = ["Colton", "Remmert", "some ID", "1/1/2000", "12/31/1999", "University of the Pacific"]

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

    def __init__(self, window):
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
            self.swapTO(mainMenu)

        else:
            messagebox.showerror("Login Unsuccessful", "Username or Password is invalid")
            self.passENTRY.delete(0,END) #remove password

def main():
    window = Tk()
    window.resizable(0,0)
    currentSCREEN = loginScreen(window)
    window.mainloop()


main()