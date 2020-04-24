import datetime
import re

dataSize = 50


def checkSpecialCharacters(in_str):
    special = re.compile('[@_!#$%^&*()<>?/\\\|}{~: 1234567890]\'\";~`-_\+=')
    in_str = str(in_str)

    return special.search(in_str) is not None


def checkDate(in_str):
    if '/' in in_str:
        if len(in_str) != 10:
            return False
        # format mm/dd/yyyy
        month, day, year = in_str.split('/')
    else:
        if len(in_str) != 8:
            return False
        month, day, year = in_str[0:2], in_str[2:4], in_str[4:8]
        # print(month,day,year)
    try:
        datetime.datetime(int(year), int(month), int(day))
        if datetime.datetime(int(year), int(month), int(day)) > datetime.datetime.now():
            return False
        return True
    except ValueError:
        return False
        # raise ValueError("Incorrect data format, should be MM/DD/YYYY")


def checkType(in_str, tp):
    # if len(in_str) > 50:
    #     return False
    if checkSpecialCharacters(in_str):
        print('contain sepcial char')
        return False
    if tp is 'int':
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
    elif tp is 'date':
        return checkDate(in_str)
    else:
        print(dataSize)
        return len(in_str) < dataSize
