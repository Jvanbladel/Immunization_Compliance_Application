from DemoGraphics import *

class Patient():
    def __init__(self, data):
        self.fName = data[0]
        self.lName = data[1]
        self.score = data[2]
        self.dueDate = data[3]
        self.MRN = data[4]
        self.daysOverDue = data[5]
        self.demoGraphic = DemoGraphics()

    def getSummary(self):
        return [self.fName, self.lName, 'D' ,"12/6/1987", 'M', "33", "African American", "Mr."]

    def getHistory(self):
        return [[["Flu", "45", "Covered"], ["Hepatitis B", "12", "Covered"], ["Pollo", "325", "Uncovered"], ["Chickpox", "15", "Uncovered"], ["MMR", "749", "Partial"], ["Rotavirus","45", "Covered"], ["Yellow Fever", "365", "Partial"]], "3/23/14"]

    def getContact(self):
        return [["(925)980-4048", "Mobile"], "austin@gmail.com", "English", "Phone"]
