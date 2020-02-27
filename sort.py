from numpy import sort

import Patients

def sortPatients(listOfPatients, fields, desc):
    '''desc == True:
            Z to A
        desc == False:
            A to Z
    '''
    """[self.fName
        self.lName
        self.score
        self.dueDate
        self.MRN
        self.daysOverDue]"""
    c = [lambda x: x.fName, lambda x: x.lName, lambda x: int(x.score), lambda x: int(x.daysOverDue),
         lambda x: int(x.MRN), lambda x: int(x.daysOverDue)]
    if fields not in [1, 2, 3, 4, 5, 6]:
        return -1

    sortedPatients = sorted(listOfPatients, key=c[fields-1], reverse=desc)
    return sortedPatients

def lastName(listOfPatients):
    character = ['abcdefghijklmnopqrstuvwxyz']
    percentage = {}
    for i in listOfPatients:
        firstChar = i.lName[0]
        if percentage.get(firstChar) is None:
            percentage[firstChar] = 1/len(listOfPatients)
        else:
            percentage[firstChar] = percentage.get(firstChar)+(1/len(listOfPatients))
    return percentage

"""    if fields == 1:
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
    return sortedPatients"""

'''
f = open("UITestData.txt", "r")
pList = []
for line in f:
    l = line.split()
    pList.append(Patients.Patient(l))
f.close()
sorted = sortPatients(pList,1,True)'''


