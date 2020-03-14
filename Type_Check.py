import datetime
import re

def checkSpecialCharacters(in_str):
    special = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if special.search(in_str) == None:
        return True
    return False
def checkDate(in_str):
    if len(in_str) != 10:
        return False
    #formate mm/dd/yyyy
    month, day, year = in_str.split('/')
    try:
        datetime.datetime(int(year), int(month), int(day))
        if datetime.datetime(int(year), int(month), int(day)) > datetime.datetime.now():
            return False
        return True
    except ValueError:
        return False
        # raise ValueError("Incorrect data format, should be MM/DD/YYYY")


def checkType(in_str, tp):
    if len(in_str) > 50:
        return False
    elif tp is 'int':
        try:
            val = int(in_str)
            print("Input is an integer number. Number = ", val)
            return True
        except ValueError:
            print("No.. input is not an integer. It's a string")
            return False
    elif tp is 'float':
        try:
            val = float(in_str)
            print("Input is a float  number. Number = ", val)
            return True
        except ValueError:
            print("No.. input is not a float. It's a string")
            return False
# print(checkDate('23/23/2323'))