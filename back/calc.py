#представьте типо расчеты

import threading as thrd

class CalculationsFund:
    def __init__(self):
        self.alert_fn = lambda ___, __: print(end='')

    def init(self, db, LIVEPARAMS):
        self.LIVEPARAMS = LIVEPARAMS
        self.db = db
        self.last = {}
        self.ll = {}
        for device in db.devices.find():
            self.last[device["uid"]] = {}
            self.last[device["uid"]]["live"] = list(db.liveparams.find({"uid": device["uid"]}).sort("timestamp"))[-1]
            self.ll[device["uid"]] = (device["lat"], device["lon"])
            del self.last[device["uid"]]["live"]["_id"]
            self.last[device["uid"]]["lake"] = list(db.probe_params.find({"device_uid": device["uid"], "probe_type": "lake"}).sort("timestamp_analises"))[-1]["params"]
            self.last[device["uid"]]["rain"] = list(db.probe_params.find({"device_uid": device["uid"], "probe_type": "rain"}).sort("timestamp_analises"))[-1]["params"]

    def __call__(self, uid: str):
        if not uid in self.last.keys():
            d = {}
            for lparam in self.LIVEPARAMS:
                d[lparam] = 0
            return d
        return self.last[uid]

fund = CalculationsFund()

def alertthis():
    def panicaaaaaaaaaaaaaaaaaaaaaaaaaaaaa(fn):
        fund.alert_fn = fn
    return panicaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

def calc_speed(last_val: float, new_val: float, last_time: float, new_time: float) -> float:
    return ( new_val - last_val ) / ( (new_time/60) - (last_time/60) )

def calc_new_vals(vals: dict):
    last_vals = fund.last[vals["uid"]]["live"]
    params = []
    for key in vals.keys():
        if key == "uid" or key == "timestamp": continue
        params.append(f"{key}Speed")
    for param in params:
        vals[param] = 0
    for key in vals.keys():
        if key == "uid" or key == "timestamp": continue
        if "Speed" in key: continue
        try: last_val = last_vals[key]
        except KeyError: last_val = 0
        vals[f"{key}Speed"] = calc_speed(last_val, vals[key], last_vals["timestamp"], vals["timestamp"])
    fund.last[vals["uid"]]["live"] = vals
    fund.db.liveparams.insert_one(vals)
    #thrd.Thread(target=check_pdk, args=(vals, )).start()

PDK_GASES = {
    "C4H10": 200,
    "C3H8": 50,
    "LPG": 300,
    "C6H6": 0.3,
    "C6H6O": 0.01
}

def check_pdk(vals: dict):
    alert = {}
    for key in vals.keys():
        try: float(vals[key])
        except Exception: continue
        if key in PDK_GASES.keys():
            if vals[key] > PDK_GASES[key]: alert[key] = [vals[key], PDK_GASES[key]]
    if alert: fund.alert_fn("gas", alert)

PDK_LAKE = {
    "Cl": 350,
    "SO4": 500,
    "NH4": 1.5,
    "NO2": 3.3,
    "NO3": 45,
    "Fe": 0.3,
    "Cu": 1,
    "Zn": 1,
    "Ni": 0.02,
    "Mg": 0.1,
    "-OH": 0.01,
    "petroleum": 0.3
}

def check_pdk_lake(vals: dict):
    alert = {}
    for key in vals.keys():
        try: float(vals[key])
        except Exception: continue
        if key in PDK_LAKE.keys():
            if vals[key] > PDK_LAKE[key]: alert[key] = [vals[key], PDK_LAKE[key]]
    if alert: fund.alert_fn("lake", alert)

PDK_RAIN = {
    "HCO3": 60,
    "SO4": 500,
    "Cl": 350,
    "NO3": 45,
    "Ca": 180,
    "Mg": 50,
    "Na": 200,
    "K": 18
}

def check_pdk_rain(vals: dict):
    alert = {}
    for key in vals.keys():
        try: float(vals[key])
        except Exception: continue
        if key in PDK_RAIN.keys():
            if vals[key] > PDK_RAIN[key]: alert[key] = [vals[key], PDK_RAIN[key]]
    if alert: 
        print("ALERT!!")
        fund.alert_fn("rain", alert)