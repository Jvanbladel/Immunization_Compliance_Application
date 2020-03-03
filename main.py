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

def main(): # Main loop of ICA
    window = Tk()
    window.resizable(0, 0)
    window.title()

    SQL = SQLConnection.SQLConnection()
    currentSCREEN = Login_Screen.loginScreen(window, None, SQL)

    #currentUser = User([0, "Jason", "Van Bladel", "Admin"], 1)
    #currentSCREEN = mainMenu(window, currentUser)

    #currentSCREEN = mainMenu(window, ["Jason Van Bladel"])
    #currentUser = User([0, "Jason", "Van Bladel", "Admin"], 1)
    #currentSCREEN = mainMenu(window, currentUser)

    #currentSCREEN = med_INFO_SCREEN(window,Patient(["John","Smith","20","2/3/2013","32","30"]))

    window.mainloop()

if __name__ == "__main__":
    main()
