import pyodbc


def main():
    # build connection with the database

    conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=;'
                            'Database=;'
                            'Trusted_Connection=yes;')

    cursor = conn.connect()

    # send sql query
    sql = '''
    SELECT *
    FROM table_1
    '''
    cursor.execute(sql)

    for row in cursor:
        print(row)
