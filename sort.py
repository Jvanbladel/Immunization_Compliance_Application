from numpy import sort
import Type_Check
import pandas as pd
import Patients
import query_generator
import SQLConnection

attributes = 8
sorted_by = [lambda x: x.fName, lambda x: x.lName, lambda x: int(x.score), lambda x: int(x.daysOverDue),
             lambda x: int(x.MRN), lambda x: x.sex, lambda x: x.immunization,
             lambda x: int(x.age)]


def sortPatients(listOfPatients, fields, desc):
    """
    desc == True:
            Z to A
        desc == False:
            A to Z
    [self.fName
        self.lName
        self.score
        self.dueDate
        self.MRN
        self.daysOverDue]
    """

    if fields not in list(range(attributes + 1)) and fields != 0:
        return -1

    sortedPatients = sorted(listOfPatients, key=sorted_by[fields - 1], reverse=desc)
    return sortedPatients


def fuzzySearch(self, field, input_str, input_type):
    if not Type_Check.checkType(input_str, input_type):
        print("invalid input")
        return
    SQLConn = SQLConnection.SQLConnection()
    query = query_generator.fuzzySearch_sql(field, input_str, input_type)
    # print(sql)
    data = pd.read_sql(query, self.conn, params={field, input_str})
    if data.empty:
        SQLConn.closeConnection()
        print("Empty Data")
        return
    plist = []
    for p in data:
        data = [p[0], p[1], p[2], p[3], None, p[4], None, None, None, None, None, None, None]
        plist.append(Patients.Patient(data))
    SQLConn.closeConnection()
    return plist


def percentages(listOfPatients):
    # character = list(map(chr, range(65, 91)))
    num_patients = len(listOfPatients)
    percentage = {}
    for i in listOfPatients:
        firstChar = i.lName[0]
        if percentage.get(firstChar) is None:
            percentage[firstChar] = round(1 / num_patients * 100, 2)
        else:
            percentage[firstChar] = percentage.get(firstChar) + round((1 / num_patients) * 100, 2)
    return percentage
