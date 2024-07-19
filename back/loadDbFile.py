import pymongo as mongo

import bson

db = mongo.MongoClient("mongodb://localhost:27017").siburopenecomap

for col in db.list_collection_names():
    db.drop_collection(col)

binary = open("db_save", 'rb').read()

data = bson.BSON.decode(binary)

for col in data.keys():
    for el in data[col]:
        db[col].insert_one(el)