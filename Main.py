# Iris
#Colton
#
from tkinter import *
from loginScreen import *
from MainMenu import *
from PatientScreen import *



def main():
    print("Hello World!")
    print("Testing")
    print("Test Push")

    window = Tk()
    window.resizable(0, 0)
    currentSCREEN = loginScreen(window, None)

    # currentSCREEN = mainMenu(window, ["Jason Van Bladel"])
    window.mainloop()


main()