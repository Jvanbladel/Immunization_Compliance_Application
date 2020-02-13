from icaScreens import *
from MainMenu import *


class loginScreen(icaSCREENS):

    def __init__(self, window, data):
        super().__init__(window)
        self.root.geometry("800x600")
        self.background = Canvas(self.root, width=800, height=600, bg="light blue")
        self.background.place(x=0, y=0)

        self.loginBackGround = Canvas(self.root, width=500, height=250)
        self.loginBackGround.place(x=150, y=275)

        self.userName = "Test01"
        self.passWord = "Test02"

        image = Image.open("sources/ica picture.PNG")
        image = image.resize((700, 200), Image.ANTIALIAS)
        self.titleIMAGE = ImageTk.PhotoImage(image)

        self.imageLABEL = Label(self.root, image=self.titleIMAGE)

        self.imageLABEL.place(x=50, y=25)

        self.userNameLabel = Label(self.root, text="Username: ", font=('Consolas', 16))
        self.userNameLabel.place(x=200, y=300)

        self.userNameEntry = Entry(self.root, width=25, font=(16))
        self.userNameEntry.place(x=350, y=305)

        self.passwordLabel = Label(self.root, text="Password: ", font=('Consolas', 16))
        self.passwordLabel.place(x=200, y=350)

        self.passwordEntry = Entry(self.root, width=25, font=(16), show="*")
        self.passwordEntry.place(x=350, y=355)

        self.loginButton = Button(self.root, text="Login!", bg="light blue", fg="black", width=13, height=2,
                                  command=self.verifyUser)
        self.loginButton.place(x=350, y=400)

        self.cancelButton = Button(self.root, text="Cancel", bg="light blue", fg="black", width=13, height=2,
                                   command=self.exitICA)
        self.cancelButton.place(x=475, y=400)

    def verifyUser(self):
        name = self.userNameEntry.get()
        passWord = self.passwordEntry.get()

        # Would hash and verify user with database here
        if name == self.userName and passWord == self.passWord:
            messagebox.showinfo("Login Successful!", "Welcome back " + str(name))
            self.swapTO(mainMenu, [self.userName])
        else:
            messagebox.showerror("Login Unsuccessful", "Username or Password is invalid")
            self.passwordEntry.delete(0, END)  # remove password
