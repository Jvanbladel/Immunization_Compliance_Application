import ICA_super
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk,Image
from Security import Hash
import Users
import Main_Menu

class loginScreen(ICA_super.icaSCREENS):

    def __init__(self, window, data, SQL):
        super().__init__(window, SQL)
        self.root.geometry("800x600")
        self.root.title("Immunization Compliance Application " + self.versionNumber)

        self.background = Canvas(self.root,width=800,height=600)
        self.background.place(x=0,y=0)

        self.bindKey("<Return>",self.enterPress)
        self.bindKey("<Escape>",self.escapePress)

        self.loginBackGround = Canvas(self.root,width=500,height=250)
        self.loginBackGround.place(x=150,y=275)

        image = Image.open("sources/ica picture.PNG")
        image = image.resize((700,200), Image.ANTIALIAS)
        self.titleIMAGE = ImageTk.PhotoImage(image)

        self.imageLABEL = Label(self.root,image=self.titleIMAGE)

        self.imageLABEL.place(x=50,y=25)


        self.userNameLabel = Label(self.root,text="Username: ",font=('Consolas', 16))
        self.userNameLabel.place(x=200,y=300)

        self.userNameEntry = Entry(self.root,width=25,font=(16))
        self.userNameEntry.place(x=350,y=305)
        self.userNameEntry.insert(0,"AUser")

        self.passwordLabel = Label(self.root, text="Password: ", font=('Consolas', 16))
        self.passwordLabel.place(x=200, y=350)
       

        self.passwordEntry = Entry(self.root, width=25, font=(16),show="*")
        self.passwordEntry.place(x=350, y=355)
        self.passwordEntry.insert(0,"Test1234#")

        self.loginButton = Button(self.root,text="Login!",bg="light blue",fg="black",width=13,height=2,command=self.verifyUser)
        self.loginButton.place(x=350,y=400)

        self.cancelButton = Button(self.root,text="Cancel",bg="light blue",fg="black",width=13,height=2,command=self.exitICA)
        self.cancelButton.place(x=475,y=400)

        self.userNameLabel = Label(self.root,text=self.versionNumber[1:-1],font=('Consolas', 16))
        self.userNameLabel.place(x=5,y=575)


        self.accountBUTTON = Button(self.root,text="Add Account",width=18,font=('Consolas', 16),bg="hot pink",command=self.createAccount)
        self.accountBUTTON.place(x=350,y=450)

    def createAccount(self): # Promts user for account creation

        newWindow = Toplevel()
        newWindow.geometry("600x600")
        newWindow.title("Account Creation")


        background = Canvas(newWindow,bg='light blue',width=600,height=600)
        background.pack()

        forground = Canvas(background,width=400,height=400)
        forground.place(x=100,y=50)

        entryLabels = ["Firstname: ","Lastname: ","Email: ","Username: ","Password: ","Confirm Pass: "]
        creationEntries = []

        yLabel = 25


        for label in entryLabels: # will fill the account creation screen with labels

            newLabel = Label(forground,text=label,font=('Consolas', 14),relief="groove",width=15)
            newLabel.place(x=25,y=yLabel)

            #newEntry = Entry(forground)

            yLabel += 50 # increment



    def verifyUser(self):
        name = self.userNameEntry.get()
        passWord = self.passwordEntry.get()

        #Would send Hash.main(name) to data base and recieve hashed pword from database
        #check if Hash.main(passWord) == recieved hashed pword

        #tempUserName = "f69ddcc92c44eb5a6320e241183ef551d9287d7fa6e4b2c77459145d8dd0bb37" # Test01

        #tempPassWord = "b575f55adf6ed25767832bdf6fe6cbc4af4889938bf48ba99698ec683f9047de" # Test02

        #tempUserName1 = "67ed235e1e075a7214902e1af0cb4bb4ad3ba0fcf084411418074cf4247004cc" # User01

        #tempPassWord1 = "7bab9c019f082639a163c437288ed2fe6da3e08a447cf9b8487f7c3535613fda" # User02

        loginUser = self.SQL.loginUser(Hash.main(name), Hash.main(passWord))
        #print(loginUser.userType)
        if not loginUser == None:
    
            messagebox.showinfo("Login Successful!", "Welcome back " + loginUser.userFirstName)#needs to be User first name
            self.removeKeyBind("<Return>")

            self.swapTO(Main_Menu.mainMenu, loginUser)#needs to be user object

        else:
            messagebox.showerror("Login Unsuccessful", "Username or Password is invalid")
            self.passwordEntry.delete(0,END) #remove password

    def enterPress(self,event):
        self.verifyUser()
