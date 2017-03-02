# -*- coding: utf-8 -*-


from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://112.74.44.140:27017")
db = client['drama']

# cursor = db.dramas.find()
# for document in cursor:
#     print(document)

# result = db.dramas.delete_many({})
# print(result.deleted_count)

# db.dramas.insert_one({
#         "title": {
#             "cn": u"吸血鬼日记",
#             "en": "Vampire Diaries Season 8"
#         },
#         "length":40,
#         "category":"horror"
# })

# result = db.restaurants.insert_one(
#     {
#         "address": {
#             "street": "2 Avenue",
#             "zipcode": "10075",
#             "building": "1480",
#             "coord": [-73.9557413, 40.7720266]
#         },
#         "borough": "Manhattan",
#         "cuisine": "Italian",
#         "grades": [
#             {
#                 "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
#                 "grade": "A",
#                 "score": 11
#             },
#             {
#                 "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
#                 "grade": "B",
#                 "score": 17
#             }
#         ],
#         "name": "Vella",
#         "restaurant_id": "41704620"
#     }
# )