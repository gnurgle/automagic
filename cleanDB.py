import sqlite3
from sqlite3 import Error


def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def delete_dup(conn):

    sql = 'SELECT DISTINCT Seq_Num FROM Base INTERSECT SELECT Seq_Num FROM Base'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()




def main():

    # create a database connection
    conn = create_connection("car_base.db")
    with conn:
        delete_dup(conn);



if __name__ == '__main__':
    main()