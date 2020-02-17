import pyodbc


def select(column, table):
    # build connection with the database

    conn = pyodbc.connect('Driver={SQL Server};\
                            Server=pacific-ica.cvb4dklzq2km.us-west-1.rds.amazonaws.com, 1433;\
                            Database=db_pacific_ica;uid=admin;pwd=Animal05')

    cursor = conn.cursor()
    print("connected")

    string = "SELECT TOP 10 "+column+" FROM " +table
    cursor.execute(string)
    # conn.commit()-- save any changes to the database
    for row in cursor:
        print(row)
    # print results

    # send sql query
    """sql = '''
    SELECT *
    FROM table_1
    '''
    cursor.execute(sql)

    for row in cursor:
        print(row)"""

    conn.close()


select("PatientID", "Patient_Table")