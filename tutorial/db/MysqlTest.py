from mysql.connector import errorcode
import mysql.connector

cnx = mysql.connector.connect(
                              user = 'root', 
                              password = '123456',
                              host = '112.74.44.140',
                              port = '3306',
                              # database='user'
)


cnx.close()