import pandas as pd
from sqlalchemy import create_engine


def main():
    # build connection with the database
    engine = create_engine('')
    # dialect[+driver]://user:password@host/dbname[?key=value..]
    # eg sql:///filename
    connection = engine.connect()

    # send sql query
    sql = '''
    SELECT *
    FROM table_1
    '''
    df = pd.read_sql_query(sql, engine)
    df