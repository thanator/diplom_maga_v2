import MySQLdb

from data.dbModel import DBModel


def readFromDb():
    mySQLconnection = MySQLdb.connection
    global modelList
    try:
        modelList = []
        mySQLconnection = MySQLdb.connect(host="localhost",  # your host
                                                        user="root",  # username
                                                        passwd="Thanator987456",  # password
                                                        db="diplom")
        sql_select_Query = "select * from pagelinks limit 10000"
        cursor = mySQLconnection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total number of rows in python_developers is - ", cursor.rowcount)
        print("Printing each row's column values i.e.  developer record")
        for row in records:
            model = DBModel(row[0], row[1], row[2], row[3])
            modelList.append(model)
        cursor.close()

    except MySQLdb.Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if mySQLconnection.open:
            mySQLconnection.close()
            print("MySQL connection is closed")
            return modelList
