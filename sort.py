from numpy import sort

import Patients

def quickSort(listOfPatients, fields):
    """[fName
        self.lName
        self.score
        self.dueDate
        self.MRN
        self.daysOverDue]"""

    if fields == 1:
        sortedPatients = sorted(listOfPatients, key=lambda x: x.fName)
    elif fields == 2:
        sortedPatients = sorted(listOfPatients, key=lambda x: x.lName)
    elif fields == 3:
        sortedPatients = sorted(listOfPatients, key=lambda x: int(x.score))
    elif fields == 4:
        sortedPatients = sorted(listOfPatients, key=lambda x: int(x.daysOverDue))
    elif fields == 5:
        sortedPatients = sorted(listOfPatients, key=lambda x: int(x.MRN))
    elif fields == 6:
        sortedPatients = sorted(listOfPatients, key=lambda x: int(x.daysOverDue))
    else:
        print("invalid field number")
        return -1
    return sortedPatients


f = open("UITestData.txt", "r")
pList = []
for line in f:
    l = line.split()
    pList.append(Patients.Patient(l))
f.close()

s = quickSort(pList, 4)

for i in range(len(pList)):
    print(s[i].dueDate)

