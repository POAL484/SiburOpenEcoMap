import typing

PDK_GASES = {
    "C4H10": 200,
    "C3H8": 50,
    "LPG": 300,
    "C6H6": 0.3,
    "C6H6O": 0.01
}

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

class PdkClass:
    def __init__(self, vals: dict, pdk: dict):
        self._class = "bunny"
        for valtype in vals.keys():
            assert valtype in pdk.keys()
            for val in vals[valtype].keys():
                if val in pdk[valtype].keys():
                    if vals[valtype][val] >= pdk[valtype][val]: self._class = "deer"
                    elif vals[valtype][val] >= pdk[valtype][val]*.8:
                        if self._class == "bunny": self._class = "bear"

class Device:
    def __init__(self, uid: str, lat: float, lon: float, last_vals: dict, timestamp_live: float, timestamp_lake: float, timestamp_rain: float):
        self.pdkClass = PdkClass({
            #"live": last_vals["live"],
            "lake": last_vals["lake"],
            "rain": last_vals["rain"]
        }, {
            #"live": PDK_GASES,
            "lake": PDK_LAKE,
            "rain": PDK_RAIN
        })
        self.uid = uid
        self.lat = lat
        self.lon = lon
        self.timestamp_live = timestamp_live
        self.timestamp_lake = timestamp_lake
        self.timestamp_rain = timestamp_rain
        self.live = last_vals['live']
        self.lake = last_vals['lake']
        self.rain = last_vals['rain']

    @classmethod
    def from_responce(self, uid: str, resp: dict):
        return Device(uid,
                      resp['ll']['lat'],
                      resp['ll']['lon'],
                      resp['values'],
                      resp['values']['live']['timestamp'],
                      resp['values']['lake']['timestamp_analises'],
                      resp['values']['rain']['timestamp_analises']
                )