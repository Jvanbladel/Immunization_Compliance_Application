class Patient:
    def __init__(self, data):
        self.fName = data[0]
        self.lName = data[1]
        self.MRN = int(data[2])
        self.score = int(data[3])
        self.status = int(data[4])
    def __str__(self):
        output = str(self.score) + " " + str(self.status) + " " + self.fName + " " + self.lName + " " + str(self.MRN)
        return output
        
class Queue:
    def __init__(self):
        self.patientList = []
        self.patientEmailList = []

    def loadQueue(self, patientList, patientEmailList):
        self.patientList = patientList
        self.patientEmailList = patientEmailList

    def addPatient(self, patient):
        if patient.score == 0 or patient.status == 0 or  patient.status == 4:
            return 0
        if patient.status == 1:
            self.patientEmailList.append(patient)
            return 1
        
        for i in range(len(self.patientList)):
            if patient.score > self.patientList[i].score:
                self.patientList.insert(i, patient)
                return 1
            
        self.patientList.append(patient)
        return 1

    def removePatient(self, MRN):
        for x in self.patientList:
            if x.MRN == MRN:
                self.patientList.remove(x)
                return 1
    
    def printQueue(self):
        print("Phone Queue:")
        for x in self.patientList:
            print(x.score, x.status, x.fName, x.lName, x.MRN)
        print("Email List:")
        for x in self.patientEmailList:
            print(x.score, x.status, x.fName, x.lName, x.MRN)
            

def main(inputF):
    q = Queue()
    file = open(inputF, 'r')
    print("Uncontacted Patients:")
    for line in file:
        pat = line.split()
        patient = Patient(pat)
        if not q.addPatient(patient):
            print(patient)
    file.close()
    print("QUEUE:")
    q.printQueue()
main("patient_test_data.txt")
