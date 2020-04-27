import SQLConnection


class Demographics():
    def __init__(self, data):
        data = data[0]
        self.address = [data[0], data[1], data[2], data[3], data[4], data[5], data[6]]
        self.demographics = [data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[20], data[16], data[17], data[15], data[19]]
        self.patientID = data[7]
        self.contact = [data[22], data[23], data[24], data[25], data[26], data[18], data[21]]
        self.guarantor = [data[30], data[29], data[31], data[32], data[28], data[22], data[23]]


class InsuranceTab():
    def __init__(self, data):
        self.insuranceName = data[0]
        self.insuranceActive = data[1]
        self.lastVisitDate = data[2]
        self.providerFirstName = data[3]
        self.providerLastName = data[4]
        self.providerNPI = data[5]

class Contact():
    def __init__(self, data):
        self.preferedLanguage = data[0]
        self.preferedContact = data[1]

    def getAdress(self):
        pass
        
class Address():
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

    class ContactNotes():
        def __init__(self, data):
            self.notes = data[0]

    # adding a comment so I can push this file.

    def getDemographics(self, sql):
        SQL.get

    def getContactNotes(self, sql):
        SQL.get

    def getInsuranceTab(self, sql):
        SQL.get

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

    def getGuarantor(self):
        return None

    def getLastService(self):
        return None

    def getFullImmunizationHistory(self):
        return None
