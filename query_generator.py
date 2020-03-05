def exactSearch_sql(self, table, field, input_str):
    sql = 'select ' + field + ' from ' + table + ' where ' + field + ' = \'' + input_str + '\''
    return sql


def fuzzySearch_sql(self, table, field, input_str):
    sql = ''
    sql += exactSearch_sql(table,field,input_str)
    i = len(input_str) - 1
    while i > 0:
        fuzzy = 'select ' + field + ' from ' + table + ' where ' + field + ' like \'' + input_str[0:i] + '%\''
        sql = sql + ' union ' + fuzzy
        i -= 1
    return sql