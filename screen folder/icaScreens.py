from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
import datetime


class icaSCREENS():
    '''
    Base class for all screens. Currently will only contain the root,
    clear the screen, and swap to other screens.
    '''

    screenSTACK = []

    def __init__(self, window):  # all screens must contain the root window
        self.root = window
        self.root.protocol("WM_DELETE_WINDOW", self.exitICA)

    def clearSCREEN(self):
        # will clear the screen of everything
        for widget in self.root.winfo_children():
            widget.destroy()

    def swapTO(self, newSCREEN, data):  # pass the class of the screen you want to go to along with the window
        self.clearSCREEN()
        newSCREEN(self.root, data)

    def exitICA(self):  # prompt user if they want to close program
        userChoice = messagebox.askyesno("Exiting ICA", "Are you sure you want to exit ICA?")

        if userChoice:
            self.root.destroy()


class Patient():
    def __init__(self, data):
        self.fName = data[0]
        self.lName = data[1]
        self.score = data[2]
        self.dueDate = data[3]
        self.MRN = data[4]
        self.daysOverDue = data[5]

    def getHistory():
        return None

    def getContact():
        return None