from ICA_super import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk,Image
from Security import Hash
import Users
from Main_Menu import *


class loginScreen(icaSCREENS):

    def __init__(self, window, data):
        super().__init__(window)
        self.root.geometry("800x600")
        global versionNumber
        self.root.title("Immunization Compliance Application " + versionNumber)

        self.background = Canvas(self.root, width=800, height=600)
        self.background.place(x=0, y=0)

        self.bindKey("<Return>", self.enterPress)
        self.bindKey("<Escape>", self.escapePress)

        self.loginBackGround = Canvas(self.root, width=500, height=250)
        self.loginBackGround.place(x=150, y=275)

        image = Image.open("sources/ica picture.PNG")
        image = image.resize((700, 200), Image.ANTIALIAS)
        self.titleIMAGE = ImageTk.PhotoImage(image)

        self.imageLABEL = Label(self.root, image=self.titleIMAGE)

        self.imageLABEL.place(x=50, y=25)

        self.userNameLabel = Label(self.root, text="Username: ", font=('Consolas', 16))
        self.userNameLabel.place(x=200, y=300)

        self.userNameEntry = Entry(self.root, width=25, font=(16))
        self.userNameEntry.place(x=350, y=305)
        self.userNameEntry.insert(0, "AUser")

        self.passwordLabel = Label(self.root, text="Password: ", font=('Consolas', 16))
        self.passwordLabel.place(x=200, y=350)

        self.passwordEntry = Entry(self.root, width=25, font=(16), show="*")
        self.passwordEntry.place(x=350, y=355)
        self.passwordEntry.insert(0, "Test1234#")

        self.loginButton = Button(self.root, text="Login!", bg="light blue", fg="black", width=13, height=2,
                                  command=self.verifyUser)
        self.loginButton.place(x=350, y=400)

        self.cancelButton = Button(self.root, text="Cancel", bg="light blue", fg="black", width=13, height=2,
                                   command=self.exitICA)
        self.cancelButton.place(x=475, y=400)

        self.userNameLabel = Label(self.root, text=versionNumber[1:-1], font=('Consolas', 16))
        self.userNameLabel.place(x=5, y=575)

        # Account creation info
        self.accountBUTTON = Button(self.root, text="Add Account", width=18, font=('Consolas', 16), bg="light blue",
                                    fg="black", command=self.createAccountScreen)
        self.accountBUTTON.place(x=350, y=450)

        self.newAccountEntries = {}  # will contain the entry boxes/info for account creation

        self.newWindow = None  # holds popout window

    def createAccountScreen(self):  # Prompts user for account creation

        if self.newWindow is not None:  # prevent multiple instances of account creation

            messagebox.showinfo("Already existing window", "Account creation page is already open")
            return

        self.newWindow = Toplevel()
        self.newWindow.geometry("600x600")
        self.newWindow.title("Account Creation")
        self.newWindow.protocol("WM_DELETE_WINDOW", self.destroyPopOut)

        background = Canvas(self.newWindow, bg='light blue', width=600, height=600)
        background.pack()

        forground = Canvas(background, width=400, height=400)
        forground.place(x=100, y=50)

        entryLabels = ["Firstname: ", "Lastname: ", "Email: ", "Username: ", "Password: ", "Confirm Pass: "]
        yLabel = 25

        for label in entryLabels:  # will fill the account creation screen with labels

            newLabel = Label(forground, text=label, font=('Consolas', 14), width=15)
            newLabel.place(x=25, y=yLabel)

            if label == "Password: " or label == "Confirm Pass: ":  # will hide password on respective entry
                newEntry = Entry(forground, font=('Consolas', 14), show="*", width=20)
                newEntry.place(x=175, y=yLabel)
            else:
                newEntry = Entry(forground, font=('Consolas', 14), width=20)
                newEntry.place(x=175, y=yLabel)

            self.newAccountEntries[label] = newEntry  # add to the new account holder
            yLabel += 50  # increment

        # buttons for submitting data and canceling account creation
        create = Button(forground, text="Create Account!", bg="light blue", fg="black", height=2,
                        command=self.createAccount)
        create.place(x=175, y=yLabel)

        cancel = Button(forground, text="Cancel", width=10, height=2, bg="light blue", fg="black",
                        command=self.newWindow.destroy)
        cancel.place(x=300, y=yLabel)

    def createAccount(self):  # will obtain info from create Account screen and pass to admin queue

        accountINFO = []  # list to be sent to admin queue

        if self.newAccountEntries["Password: "].get() == self.newAccountEntries["Confirm Pass: "].get():

            for info in self.newAccountEntries:

                thisINFO = self.newAccountEntries[info].get()

                if not thisINFO:  # will determine if there is data in this entry

                    messagebox.showwarning("Missing Field", "Missing field:\n" + info)
                    return

                accountINFO.append(thisINFO)

            messagebox.showinfo("account sent", "Sent to admin for approval")
            self.destroyPopOut()

        else:
            messagebox.showinfo("do not match", "passwords do not match")

    def clearAccount(self):  # clears entries for account creation on sent info

        for entry in self.newAccountEntries:
            self.newAccountEntries[entry].delete(0, 'end')

    def destroyPopOut(self):  # helps manage only one window at a time

        self.newWindow.destroy()
        self.newWindow = None
        self.newAccountEntries.clear()

    def verifyUser(self):
        name = self.userNameEntry.get()
        passWord = self.passwordEntry.get()

        # Would send Hash.main(name) to data base and recieve hashed pword from database
        # check if Hash.main(passWord) == recieved hashed pword

        # tempUserName = "f69ddcc92c44eb5a6320e241183ef551d9287d7fa6e4b2c77459145d8dd0bb37" # Test01

        # tempPassWord = "b575f55adf6ed25767832bdf6fe6cbc4af4889938bf48ba99698ec683f9047de" # Test02

        # tempUserName1 = "67ed235e1e075a7214902e1af0cb4bb4ad3ba0fcf084411418074cf4247004cc" # User01

        # tempPassWord1 = "7bab9c019f082639a163c437288ed2fe6da3e08a447cf9b8487f7c3535613fda" # User02

        loginUser = self.SQL.loginUser(Hash.main(name), Hash.main(passWord))
        # print(loginUser.userType)
        if not loginUser == None:

            messagebox.showinfo("Login Successful!",
                                "Welcome back " + loginUser.userFirstName)  # needs to be User first name
            self.removeKeyBind("<Return>")

            self.swapTO(mainMenu, loginUser)  # needs to be user object

        else:
            messagebox.showerror("Login Unsuccessful", "Username or Password is invalid")
            self.passwordEntry.delete(0, END)  # remove password

    def enterPress(self, event):
        self.verifyUser()
