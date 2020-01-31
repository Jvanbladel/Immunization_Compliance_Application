import random
import string
import  time

#loads all values from text file to list

def loadFileValues(file):
    f = open(file, 'r')
    output = []
    for line in f:
        output.append(line.split("\n")[0])
    f.close()
    return output

#generates a random first name and gender

def randomFirstName(male, female):
    if random.random() > .51:
        return random.choice(male), 'M'
    return random.choice(female), 'F'

#generates a random last name

def randomLastName(lastnames):
    return random.choice(lastnames)

#generates a random person with first name, last name and sex

def randomPerson(male, female, lastnames):
    fname, sex = randomFirstName(male, female)
    lname = randomLastName(lastnames)
    return fname, lname, sex

#generates a random number between 2 ranges

def randomIntField(low, high):
    return int((high-low+1)*random.random()+low)

#creates a random string of char for a defined length

def randomStringField(length):
    output = str()
    for x in range(length):
        output = output + randomChar()
    return output

#returns a random character
        
def randomChar():
    return random.choice(string.ascii_letters)

#helper method for choosing a random date, does not work for dates eariler than 1970

def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

#returns a random date between 2 ranges, does not work for dates eariler than 1970

def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)

#generates a random date between 1972 and 2100

def randomDate():
    return random_date("1/1/1972 1:30 PM", "1/1/2100 4:50 AM", random.random())

#generates a random phone number

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

# returns random number between 1-9, does not include 0

def randomNumber():
    nums = "123456789"
    return random.choice(nums)

#returns a random gmail address of length 15

def randomEmail():
    string = randomStringField(15)
    string = string + "@gmail.com"
    return string 

#returns 1 or 0

def randomBoolean():
    if random.random() > .5:
        return 0
    return 1

#prints menu
    
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
    print("0) Exit")

#method for creating a single data point

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

#function returns data to specified output file

def sendDataToTxt(filename, data):
    f = open(filename, "w")
    for x in data:
        line = str(x[0])
        for i in range(len(x)-1):
            line = line + " " + str(x[i+1])
        line = line + "\n"
        f.write(line)
    f.close()

#loops unitl user enters valid int 

def getIntFromUser(question):
    dataInput = None
    while dataInput == None:
        print(question)
        dataInput = input("Enter interger: ")
        if dataInput.isdigit():
            return int(dataInput)
        else:
            dataInput = None

#loops unitl user enters valid Y or N
            
def getYorNFromUser(question):
    dataInput = None
    while dataInput == None:
        print(question)
        dataInput = input("Enter Y or N: ")
        dataInput = dataInput.upper()
        if dataInput == 'Y' or dataInput == 'N':
            return dataInput
        else:
            dataInput = None

#Logic for program

def main():

    #loads files for generating names
    
    males = loadFileValues("male-first-names.txt")
    females = loadFileValues("female-first-names.txt")
    lastnames = loadFileValues("last-names.txt")

    
    print("Welcome to the random data generator")
    answer = str()

    #datafields are the inputs the user enters

    dataFields = []
    #quits when user enters 0
    while answer != 0:
        printMenu()
        answer = getIntFromUser("")
        #1 is for creating a new person
        if answer == 1:
            a1 = getYorNFromUser("\nWould you like FirstNames?\n")
            a2 = getYorNFromUser("\nWould you like lastNames?\n")
            a3 = getYorNFromUser("\nWould you like sex of individual?\n")
            dataFields.append((answer, a1,a2,a3))
        #2 is for creating a new int
        elif answer == 2:
            a1 = getYorNFromUser("\nWould you like the integer to have repeats?\n")
            if a1 == 'Y':
                a2 = getIntFromUser("\nEnter lowest range.\n")
                a3 = getIntFromUser("\nEnter highest range.\n")
                dataFields.append((answer, a1,a2,a3))
            else:
                dataFields.append((answer, a1))
        #3 is for creating a new string
        elif answer == 3:
            a1 = getIntFromUser("\nHow long should the string be?\n")
            dataFields.append((answer, a1))
        #4 is for creating everything else
        elif answer != 0:
            dataFields.append((answer, ""))

    #Get file name and amount of data points
    numb = getIntFromUser("\nHow data point would you like?\n")
    filename = input("\nEnter Text File To Create: (include .txt)\n")

    #gernerates random data point
    finalData = []
    for y in range(numb):
        v = randomData(dataFields, males, females, lastnames)
        print(v)

        finalData.append(v)

    #exports data to specified file
    sendDataToTxt(filename, finalData)

index = 1 
main()
