#made from copy pasted code
import os
import sqlite3

from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def LoadDatas(conn):
    """
    Query all rows in the userdata table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM userdata")

    rows = cur.fetchall()

    #for row in rows:
    #    print(row)
    return rows

def AddData(conn, project):
    """
    Create a new project into the userdata table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO userdata(name,jk,umur,waktu,berat,tinggi,status)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def DbInit(dirs="apeks.db"):
    database = dirs

    print("Check DB..")
    if not os.path.exists(dirs):
        print("DB Not Exists Creating DB")

        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS userdata (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            jk text NOT NULL,
                                            umur integer NOT NULL,
                                            waktu text NOT NULL,
                                            berat text NOT NULL,
                                            tinggi text NOT NULL,
                                            status text NOT NULL
                                        ); """

        # create a database connection
        conn = create_connection(database)

        # create tables
        if conn is not None:
            # create projects table
            create_table(conn, sql_create_projects_table)

            # create tasks table
            #create_table(conn, sql_create_tasks_table)
        else:
            print("Error! cannot create the database connection.")
    else:
        print("DB Is Exists")



if __name__ == '__main__':
    DbInit()
