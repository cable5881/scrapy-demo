from pymongo import MongoClient
import mysql.connector

url = "mongodb://112.74.44.140:27017"
db_name = "drama"

class mongoDb(object):
	def __init__(self):
		client = MongoClient(url)
		self.db = client[db_name]
		
	def insert_one(self, drama):
		self.db.dramas.insert_one(drama)

		
conn = mysql.connector.connect(user='root', password='123456', database='test')
cursor = conn.cursor()
cursor.execute('select * from city')
values = cursor.fetchall()
print(values)
