import pymongo as mongo

import bson

db = mongo.MongoClient("mongodb://localhost:27017").siburopenecomap

data = {}

for col in db.list_collection_names():
    data[col] = []
    for el in db[col].find():
        data[col].append(el)

with open("db_save", 'wb') as fp:
    fp.write(bson.BSON.encode(data))
    fp.close()