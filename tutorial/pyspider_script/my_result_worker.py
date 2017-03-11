from pyspider.result import ResultWorker
from pymongo import MongoClient

# pyspider result_worker --result-cls=my_result_worker.MyResultWorker

client = MongoClient("mongodb://112.74.44.140:27017")
db = client['drama']

class MyResultWorker(ResultWorker):
	def on_result(self, task, result):
        # assert task['taskid']
        # assert task['project']
        # assert task['url']
        # assert result
        # your processing code goes here
		db.dramas.insert_one(result)
