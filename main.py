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

    sql = SQLConnection.SQLConnection()
    #currentUser = Users.User([0, "Jason", "Van Bladel", "Admin", 1], 1, sql)
    #currentUser.setPermissions(Users.Permissions(["Hi", "decr", 1,1,1,1,1,1,1,1,1,1,1,1,1,1, 7, 10]))
    #currentSCREEN = Main_Menu.mainMenu(window, currentUser)

    #currentSCREEN = mainMenu(window, ["Jason Van Bladel"])
    #currentUser = User([0, "Jason", "Van Bladel", "Admin"], 1)
    #currentSCREEN = mainMenu(window, currentUser)


    #test patient information for med info screen since DB is down
    testPatientData = [20,10,"Test","Account","L","4/31/2000","F","No","4/21/2020",0,"Insert Race", "Insert ethnicity",20]
    testPatient = Patient(testPatientData)

    #currentSCREEN = Med_Info_Screen.med_INFO_SCREEN(window,testPatient)
    window.mainloop()

if __name__ == "__main__":
    main()
