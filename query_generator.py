
tables = 'Patient Left Outer Join ServiceDetails On Patient.PatientId = ServiceDetails.PatientId'

def exactSearch_sql(field, input_str):
    select = ['PatientID', 'PatientMRN', 'PatientLastName', 'PatientFirstName', 'PatientDateOfBirth']
    temp_id = select.index(field)
    temp = field
    select[0] = field
    select[temp_id] = temp

    f = ' '
    for ta in select:
        if select.index(ta) == len(select)-1:
            f += ta
        else:
            f += ta +','

    sql = 'select Patient.PatientID, PatientMRN, PatientLastName, PatientFirstName, PatientDateOfBirth' + ' from ' + tables + \
          ' where ' + field + '=\'' + input_str + '\''
    return sql


def fuzzySearch_sql(field, input_str):
    select = ['PatientID', 'PatientMRN', 'PatientLastName', 'PatientFirstName', 'PatientDateOfBirth']
    sql = ''
    sql += exactSearch_sql(field, input_str)
    i = len(input_str) - 1

    temp_id = select.index(field)
    temp = field
    select[0] = field
    select[temp_id] = temp

    f = ' '
    for ta in select:
        if select.index(ta) == len(select) -1:
            f+= ta
        else:
            f += ta +', '

    while i > 0:
        fuzzy = 'select Patient.PatientID, PatientMRN, PatientLastName, PatientFirstName, PatientDateOfBirth  ' \
                ' from ' + tables + ' where ' + field + ' like \''+ str(input_str[0:i])+ '%\''
        sql = sql + ' union ' + fuzzy
        i -= 1
    print(f)
    return sql

def getAttribute_sql(table):
    return 'select column_Name from information_schema.columns where ' + table

def updateDB(table):
    return ''