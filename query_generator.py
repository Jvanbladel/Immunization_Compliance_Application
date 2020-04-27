tables = 'Patient'


def exactSearch_sql(field, input_str, input_type):
    if input_type == 'num':
        input_str = int(input_str)
    elif input_type == 'date':
        return 'select Patient.PatientID, PatientMRN, PatientLastName, PatientFirstName, PatientDateOfBirth' + ' from ' \
               + tables + ' where WHERE cast (datediff (day, 0,  + PatientDateOfBirth) as datetime) =' + input_str
    return 'select Patient.PatientID, PatientMRN, PatientLastName, PatientFirstName, PatientDateOfBirth' + ' from ' \
           + tables + ' where ' + field + '=\'' + input_str + '\''


def fuzzySearch_sql(field, input_str, input_type):

    i = len(input_str)

    sql = 'select p.PatientId,p.PatientMRN,p.PatientLastName,p.PatientFirstName,p.PatientMiddleInitial,\
            p.PatientDateOfBirth,p.PatientGender,p.DeceasedStatus,Convert(VARCHAR(10),DateAdd(year, 1, Max(s.DateofService)),101) As DueDate,\
            DateDiff(day, Max(s.DateofService), GetDate()) - 365 As Daysoverdue,p.PatientRace,p.PatientEthnicity,\
            datediff(year, max(p.PatientDateOfBirth), getdate()) As Age\
            From Patient p Left Outer Join\
            ServiceDetails s On p.PatientId = s.PatientId\
            where p.'
    if input_type is "date":
        if '/' not in input_str:
            input_str = input_str[:2]+'/'+input_str[2:4]+'/'+input_str[4:8]
        sql = sql + field + '=\'' + input_str + '\''
        return sql + ' Group By\
            p.PatientId,\
            p.PatientMRN,\
            p.PatientLastName,\
            p.PatientFirstName,\
            p.PatientMiddleInitial,\
            p.PatientDateOfBirth,\
            p.PatientGender,\
            p.DeceasedStatus,\
            p.PatientRace,\
            p.PatientEthnicity,\
            p.PreferredLanguage'
    else:
        sql = sql + field + '=\'' + input_str + ' \''

    while i > 0:
        fuzzy = ' or p.' + field + ' like \'' + str(input_str[0:i]) + '%\''
        sql = sql + fuzzy
        i -= 1

    return sql +' Group By\
            p.PatientId,\
            p.PatientMRN,\
            p.PatientLastName,\
            p.PatientFirstName,\
            p.PatientMiddleInitial,\
            p.PatientDateOfBirth,\
            p.PatientGender,\
            p.DeceasedStatus,\
            p.PatientRace,\
            p.PatientEthnicity,\
            p.PreferredLanguage'


def getAttribute_sql(table):
    return 'select column_Name from information_schema.columns where ' + table
