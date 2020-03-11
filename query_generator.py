
tables = 'Patient'

def exactSearch_sql(field, input_str):
    return 'select Patient.PatientID, PatientMRN, PatientLastName, PatientFirstName, PatientDateOfBirth' + ' from ' \
          + tables + ' where ' + field + '=\'' + input_str + '\''


def fuzzySearch_sql(field, input_str):
    sql = ''
    sql += exactSearch_sql(field, input_str)
    i = len(input_str) - 1

    while i > 0:
        fuzzy = 'select Patient.PatientID, PatientMRN, PatientLastName, PatientFirstName, PatientDateOfBirth  ' \
                ' from ' + tables + ' where ' + field + ' like \'' + str(input_str[0:i]) + '%\''
        sql = sql + ' union ' + fuzzy
        i -= 1
    return sql

def getAttribute_sql(table):
    return 'select column_Name from information_schema.columns where ' + table
