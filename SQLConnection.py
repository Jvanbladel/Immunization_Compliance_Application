import psycopg2

connection = psycopg2.connect(
    host = "pacific-ica.cvb4dklzq2km.us-west-1.rds.amazonaws.com",
    port = '1433',
    database = "db_pacific_ica",
    user="admin",
    password = "Animal05"
)

connection.set_session(autocommit=True)

with connection.cursor() as cursor:
    cursor.executue('SELECT COUNT(*) FROM patient')
    result = cursor.fetchone()

    print(result)
