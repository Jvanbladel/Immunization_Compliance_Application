import SQLConnection


class Demographics():
    def __init__(self, data):
        pass

class Garantor():
    def __init__(self, data):
        pass

class Insurence():
    def __init__(self, data):
        pass

class Contact():
    def __init__(self, data):
        self.preferedLanguage = data[0]
        self.preferedContact = data[1]

    def getAdress(self):
        pass
        
class Adress():
    def __init__(self, data):
        self.street = data[0]
        self.street2 = data[1]
        self.city = data[2]
        self.state = data[3]
        self.zipcode = data[4]
        self.county = data[5]
        self.country = data[6]
        self.addressType = data[7]
        self.badAddressIndicator = data[8]
        


class Patient():
    def __init__(self, data):
        self.patientID = data[0]
        self.MRN = data[1]
        self.lName = data[2]
        self.fName = data[3]
        self.mInitial = data[4]
        self.dob = data[5]
        self.sex = data[6]
        self.patientDead = data[7]
        self.dueDate = data[8]
        self.daysOverDue = data[9]
        self.race = data[10]
        self.ethnicity = data[11]
        self.age = str(data[12])
        
        self.prefix = ""
        if self.sex == "M":
            self.prefix = "Mr."
        elif self.sex == "F":
            self.prefix = "Ms."

    # adding a comment so I can push this file.

    def getDemographics(self):
        pass
    def getSummary(self):
        return [self.fName, self.lName, self.mInitial ,self.dob, self.sex, self.age, self.race, self.prefix]

    def getHistory(zelf):
        return [[["Flu", "45", "Covered"], ["Hepatitis B", "12", "Covered"], ["Pollo", "325", "Uncovered"], ["Chickpox", "15", "Uncovered"], ["MMR", "749", "Partial"], ["Rotavirus","45", "Covered"], ["Yellow Fever", "365", "Partial"]], "3/23/14"]

    def getContact(self):
        return [["(925)980-4048", "Mobile"], "austin@gmail.com", "English", "Phone"]

        # adding a comment so I can push this file.

    def getFullSummary(self):

        #demographics object
        return None

    def getFullHistory(self):

        #service list
        return None

    def getFullContact(self):

        #contact object
        return None

    def getFullInsurance(self):

        #insurence object
        return None

    def getGarentor(self):
        return None

    def getLastService(self):
        return None

    def getFullImmunizationHistory(self):
        return None
