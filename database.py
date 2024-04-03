#use this file for creating the following:
#1.creating connection
#2.creating database
#3.creating table
#4.describe table

from mysql.connector import connect, Error

try:
    with connect(
        host="host",
        user="user",
        password="password",
        database = "database"
    ) as connection:
        show_table_query = """
describe shop_data

"""
        with connection.cursor() as cursor:
            cursor.execute(show_table_query)
            result = cursor.fetchall()
            for row in result:
                print(row)
except Error as e:
    print(e)