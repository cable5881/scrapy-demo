from mysql.connector import errorcode
import mysql.connector

cnx = mysql.connector.connect(
    user='root',
    password='123456',
    host='localhost',
    port='3306',
    database='tv_drama_resys'
)
cursor = cnx.cursor()
cursor.execute('select * from meiju_drama')
values = cursor.fetchall()
print(values)
cnx.close()
