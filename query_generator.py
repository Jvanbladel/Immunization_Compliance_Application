def exactSearch_sql(table, field, input_str):
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

    sql = 'select p.PatientId,p.PatientMRN,p.PatientLastName,p.PatientFirstName,p.PatientMiddleInitial,p.PatientDateOfBirth,p.PatientGender,p.DeceasedStatus,Convert(VARCHAR(10),DateAdd(year, 1, Max(s.DateofService)),101) As DueDate,DateDiff(day, Max(s.DateofService),GetDate()) - 365 As Daysoverdue,p.PatientRace,p.PatientEthnicity,datediff(year, max(p.PatientDateOfBirth), getdate()) As Age where ' + field + ' like \'' + input_str[0:i] + '%\'' from ' + table + ' where ' + field + ' = \'' + input_str + '\''
    return sql


def fuzzySearch_sql(table, field, input_str):
    select = ['PatientID', 'PatientMRN', 'PatientLastName', 'PatientFirstName', 'PatientDateOfBirth']
    sql = ''
    sql += exactSearch_sql(table, field, input_str)
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
        fuzzy = 'select p.PatientId,p.PatientMRN,p.PatientLastName,p.PatientFirstName,p.PatientMiddleInitial,\
        p.PatientDateOfBirth,p.PatientGender,p.DeceasedStatus,\
        Convert(VARCHAR(10),DateAdd(year, 1, Max(s.DateofService)),101) As DueDate,DateDiff(day, Max(s.DateofService), \
        GetDate()) - 365 As Daysoverdue,p.PatientRace,p.PatientEthnicity,\
        datediff(year, max(p.PatientDateOfBirth), getdate()) As Age where ' + field + ' like \'' + input_str[0:i] + '%\''
        sql = sql + ' union ' + fuzzy
        i -= 1
    print(f)
    return sql

def getAttribute_sql(table):
    return 'select column_Name from information_schema.columns where ' + table

def updateDB(table):
    return ''