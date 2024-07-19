import pymongo as mongo

import bson

db = mongo.MongoClient("mongodb://185.211.170.46:50511").siburopenecomap

for col in db.list_collection_names():
    db.drop_collection(col)

binary = open("db_save", 'rb').read()

data = bson.BSON.decode(binary)

for col in data.keys():
    for el in data[col]:
        db[col].insert_one(el)