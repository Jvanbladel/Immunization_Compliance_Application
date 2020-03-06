from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk,Image
import datetime
from tkinter import ttk
from Patients import *
import sort
import SQLConnection
import ICA_super
import Login_Screen
import Main_Menu
import Med_Info_Screen
import Users 

def main(): # Main loop of ICA
    window = Tk()
    window.resizable(0, 0)
    window.title()

    currentSCREEN = Login_Screen.loginScreen(window, None)

    #sql = SQLConnection.SQLConnection()
    #currentUser = Users.User([0, "Jason", "Van Bladel", "Admin", 1], 1, sql)
    #currentUser.setPermissions(Users.Permissions(["Hi", "decr", 1,1,1,1,1,1,1,1,1,1,1,1,1,1, 7, 10]))
    #currentSCREEN = Main_Menu.mainMenu(window, currentUser)

    #currentSCREEN = mainMenu(window, ["Jason Van Bladel"])
    #currentUser = User([0, "Jason", "Van Bladel", "Admin"], 1)
    #currentSCREEN = mainMenu(window, currentUser)

    #currentSCREEN = Med_Info_Screen.med_INFO_SCREEN(window,Patient(["John","Smith","20","2/3/2013","32","30"]),SQL)

    window.mainloop()

if __name__ == "__main__":
    main()
