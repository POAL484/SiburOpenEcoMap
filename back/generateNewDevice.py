import pymongo as mongo
import uuid
import random
import datetime as dt

LIVE_PARAMS_DEVICED = [
    "temp",
    "pressure",
    "C4H10",
    "C3H8",
    "LPG",
    "C6H6",
    "C6H6O"
]

LIVE_PARAMS = []
for param in LIVE_PARAMS_DEVICED:
    LIVE_PARAMS.append(param)
    LIVE_PARAMS.append(f"{param}Speed")

PROBE_RAIN = [
    "HCO3",
    "SO4",
    "Cl",
    "NO3",
    "Ca",
    "Mg",
    "Na",
    "K"
]

PROBE_LAKE = [
    "Cl",
    "SO4",
    "NH4",
    "NO2",
    "NO3",
    "Fe",
    "Cu",
    "Zn",
    "Ni",
    "Mg",
    "-OH",
    "petroleum"
]

db = mongo.MongoClient("mongodb://siburok.ru:50511").siburopenecomap

tokenlist = list(str(uuid.uuid4())+str(uuid.uuid4()))
random.shuffle(tokenlist)
token = ''.join(tokenlist)

lat = float(input("lat > "))
lon = float(input("lon > "))

uid = str(uuid.uuid4())

new_device = {
    "uid": uid,
    "token": token,
    "is_probe_rain": False,
    "is_probe_lake": False,
    "lat": lat,
    "lon": lon
}

live = {}
for param in LIVE_PARAMS:
    live[param] = 0
lake = {"values": {}}
for param in PROBE_LAKE:
    lake['values'][param] = 0
rain = {"values": {}}
for param in PROBE_RAIN:
    rain['values'][param] = 0

live['uid'] = uid
live['timestamp'] = dt.datetime.now().timestamp()

lake['uid'] = str(uuid.uuid4())
lake['device_uid'] = uid
lake['ll'] = {'lat': lat, 'lon': lon}
lake['probe_type'] = "lake"
lake['timestamp_taken'] = dt.datetime.now().timestamp() - 60
lake['timestamp_analises'] = dt.datetime.now().timestamp()

rain['uid'] = str(uuid.uuid4())
rain['device_uid'] = uid
rain['ll'] = {'lat': lat, 'lon': lon}
rain['probe_type'] = "rain"
rain['timestamp_taken'] = dt.datetime.now().timestamp() - 60
rain['timestamp_analises'] = dt.datetime.now().timestamp()

db.devices.insert_one(new_device.copy())
db.liveparams.insert_one(live.copy())
db.probe_params.insert_one(lake.copy())
db.probe_params.insert_one(rain.copy())

print()
print("New device successfully registred!")
print(f"Device UID:     {uid}")
print(f"Token:          {token}")
print()