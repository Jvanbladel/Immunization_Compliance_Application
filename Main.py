from tkinter import *
from loginScreen import *
from MainMenu import *
from PatientScreen import *

versionNumber = "Immunization Compliance Application Alpha 1.1"

def main(): # Main loop of ICA
    window = Tk()
    window.resizable(0, 0)
    window.title(versionNumber)

    currentSCREEN = loginScreen(window, None)

    # currentSCREEN = mainMenu(window, ["Jason Van Bladel"])
    window.mainloop()

main()