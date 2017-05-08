from pymongo import MongoClient

url = "mongodb://112.74.44.140:27017"
db_name = "meiju"


class mongoDb(object):
    def __init__(self):
        client = MongoClient(url)
        self.db = client[db_name]

    def insert_one(self, drama):
        self.db.dramas.insert_one(drama)
