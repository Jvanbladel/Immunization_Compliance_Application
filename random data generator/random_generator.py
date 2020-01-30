import random
import string
import  time

def loadFileValues(file):
    f = open(file, 'r')
    output = []
    for line in f:
        output.append(line.split("\n")[0])
    f.close()
    return output

def randomFirstName(male, female):
    if random.random() > .51:
        return random.choice(male), 'M'
    return random.choice(female), 'F'

def randomLastName(lastnames):
    return random.choice(lastnames)

def randomPerson(male, female, lastnames):
    fname, sex = randomFirstName(male, female)
    lname = randomLastName(lastnames)
    return fname, lname, sex

def randomIntField(low, high):
    return int((high-low+1)*random.random()+low)

def randomStringField(length):
    output = str()
    for x in range(length):
        output = output + randomChar()
    return output
        
def randomChar():
    return random.choice(string.ascii_letters)

def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)

def randomDate():
    return random_date("1/1/1972 1:30 PM", "1/1/2100 4:50 AM", random.random())

def randomPhoneNumber():
    number = str()
    for x in range(3):
        number = number + str(randomNumber())
    number = number + "-"
    for x in range(3):
        number = number + str(randomNumber())
    number = number + "-"
    for x in range(4):
        number = number + str(randomNumber())
    return number

def randomNumber():
    nums = "123456789"
    return random.choice(nums)

def randomEmail():
    string = randomStringField(15)
    string = string + "@gmail.com"
    return string 

def randomBoolean():
    if random.random() > .5:
        return 0
    return 1
    
def printMenu():
    print("Would you like to generate another field?")
    print("1) Person")
    print("2) Integer")
    print("3) String")
    print("4) Char")
    print("5) Date")
    print("6) Phone Number")
    print("7) Email")
    print("8) Boolean")
    print("0) Exit\n")

def randomData(dataFields, male, female, lastnames):
    global index
    data = []
    for field in dataFields:
        if field[0] == 1:
            fname, lname, sex = randomPerson(male, female, lastnames)
            if field[1] == 'Y':
                data.append(fname)
            if field[2] == 'Y':
                data.append(lname)
            if field[3] == 'Y':
                data.append(sex)
        elif field[0] == 2:
            if field[1] == 'N':
                data.append(index)
                index += 1
            else:
                data.append(randomIntField(field[2], field[3])) 
        elif field[0] == 3:
             data.append(randomStringField(field[1]))
        elif field[0] == 4:
             data.append(randomChar())
        elif field[0] == 5:
             data.append(randomDate().split()[0])
        elif field[0] == 6:
             data.append(randomPhoneNumber())
        elif field[0] == 7:
             data.append(randomEmail())
        elif field[0] == 8:
             data.append(randomBoolean())
        
    return data

def sendDataToTxt(filename, data):
    f = open(filename, "w")
    for x in data:
        line = str(x[0])
        for i in range(len(x)-1):
            line = line + " " + str(x[i+1])
        line = line + "\n"
        f.write(line)
    f.close()
    
def main():
    males = loadFileValues("male-first-names.txt")
    females = loadFileValues("female-first-names.txt")
    lastnames = loadFileValues("last-names.txt")

    print("Welcome to the random data generator")
    answer = str()

    dataFields = []
    while answer != 0:
        printMenu()
        answer = int(input(""))
        if answer == 1:
            a1 = input("Would you like FirstNames?\nY/N: ")
            a2 = input("Would you like lastNames?\nY/N: ")
            a3 = input("Would you like sex of individual?\nY/N: ")
            dataFields.append((answer, a1,a2,a3))
        elif answer == 2:
            a1 = input("Would you like the integer to have repeats?\nY/N: ")
            if a1 == 'Y':
                a2 = int(input("Enter lowest range: "))
                a3 = int(input("Enter highest range: "))
                dataFields.append((answer, a1,a2,a3))
            else:
                dataFields.append((answer, a1))
        elif answer == 3:
            a1 = int(input("How long should the string be?\n"))
            dataFields.append((answer, a1))
        elif answer != 0:
            dataFields.append((answer, ""))
    numb = int(input("Enter number of elements: "))
    filename = input("Enter Text File To Create: (include .txt)\n")
    
    finalData = []
    for y in range(numb):
        v = randomData(dataFields, males, females, lastnames)
        print(v)

        finalData.append(v)
    sendDataToTxt(filename, finalData)

index = 1 
main()
