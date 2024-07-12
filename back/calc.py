#представьте типо расчеты

import threading as thrd

class CalculationsFund:
    def __init__(self):
        self.alert_fn = lambda: print(end='')

    def init(self, db, LIVEPARAMS):
        self.LIVEPARAMS = LIVEPARAMS
        self.db = db
        self.last = []
        self.ll = {}
        for device in db.devices.find():
            self.last.append(
                list(db.liveparams.find({"uid": device["uid"]}).sort("timestamp"))[-1]
            )
            self.ll[device["uid"]] = (device["lat"], device["lon"])
            del self.last[-1]["_id"]

    def __call__(self, uid: str):
        if not uid in self.last.keys():
            d = {}
            for lparam in self.LIVEPARAMS:
                d[lparam] = 0
            return d
        return self.last[uid]
    
    def alertthis(self):
        def panicaaaaaaaaaaaaaaaaaaaaaaaaaaaaa(fn):
            self.alert_fn = fn
        return panicaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

fund = CalculationsFund()

def calc_new_vals(vals: dict):
    last_vals = fund.last[vals["uid"]]
    vals["tempSpeed"] = ( vals["temp"] - last_vals["temp"] ) / ( (vals["timestamp"]/60) - (last_vals["timestamp"]/60) )
    vals["humiditySpeed"] = ( vals["humidity"] - last_vals["humidity"] ) / ( ( vals["timestamp"]/60) - (last_vals["timestamp"]/60) )
    vals["lightSpeed"] = ( vals["light"] - last_vals["light"] ) / ( (vals["timestamp"]/60) - (last_vals["timestamp"]/60) )
    vals["gasSpeed"] = ( vals["gas"] - last_vals["gas"] ) / ( ( vals["timestamp"]/60) - (last_vals["timestamp"]/60) )
    fund.last = vals
    fund.db.liveparams.insert_one(vals)
    thrd.Thread(target=check_pdk, args=(vals, )).start()

def check_pdk(vals: dict):
    pass

def check_pdk_lake(vals: dict):
    pass

def check_pdk_rain(vals: dict):
    pass