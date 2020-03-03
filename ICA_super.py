from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

versionNumber = "(Version 2.0.0)"

class icaSCREENS():
    '''
    Base class for all screens. Currently will only contain the root,
    clear the screen, and swap to other screens.
    '''
    screenSTACK = []
    def __init__(self,window, SQL): #all screens must contain the root window
        global versionNumber
        self.versionNumber = versionNumber
        self.root = window
        self.root.protocol("WM_DELETE_WINDOW", self.exitICA)
        # insert as "<KEYTYPE>",functionCall.
        self.keyBinds = {}
        self.SQL = SQL
        

    def clearSCREEN(self):
        #will clear the screen of everything
        for widget in self.root.winfo_children():
            widget.destroy()

    def swapTO(self,newSCREEN, data): #pass the class of the screen you want to go to along with the window
        self.clearSCREEN()
        newSCREEN(self.root, data, self.SQL)

    def bindKey(self,key,functionCall): # pass a key you want to bind and the function it should call

        self.root.bind(key,functionCall)
        self.keyBinds[key] = functionCall

    def removeKeyBind(self,key): # will remove the bind and free the key for another bind

        self.root.unbind(key)
        del self.keyBinds[key]

    def rebindKey(self,key,functionCall): # will rebind the key to another feature

        self.root.unbind(key)
        self.bindKey(key,functionCall)

    def exitICA(self): #prompt user if they want to close program

        userChoice = messagebox.askyesno("Exiting ICA","Are you sure you want to exit ICA?")

        if userChoice:
            self.SQL.closeConnection()
            self.root.destroy()

    def escapePress(self,event):
        self.exitICA()
