import Patients

def sortPatient(listOfPatients, fields):
    """fields
        1: fName
        2: lName
        3: score
        4: dueDate
        5: MRN
        6: daysOverDue"""

    if fields == 1:
        sortedPatients = sorted(listOfPatients, key=lambda x: x.fName)
    elif fields == 2:
        sortedPatients = sorted(listOfPatients, key=lambda x: x.lName)
    elif fields == 3:
        sortedPatients = sorted(listOfPatients, key=lambda x: x.score)
    elif fields == 4:
        sortedPatients = sorted(listOfPatients, key=lambda x: x.dueDate)
    elif fields == 5:
        sortedPatients = sorted(listOfPatients, key=lambda x: x.MRN)
    elif fields == 6:
        sortedPatients = sorted(listOfPatients, key=lambda x: x.daysOverDue)
    else:
        print("invalid field number")
        return -1
    return sortedPatients

