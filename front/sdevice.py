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
    def __init__(self, val_to_pdk: dict):
        self._class = "bunny"
        for vals in val_to_pdk.keys():
            pdk = val_to_pdk[vals]
            for val_name in vals.keys():
                try: pdk[val_name]
                except KeyError:
                    continue
                if vals[val_name] >= pdk[val_name]: self._class = "deer"
                elif vals[val_name] >= pdk[val_name]*0.8:
                    if self._class == "bunny": self._class = "bear"

class Device:
    def __init__(self, uid: str, lat: float, lon: float, last_vals: dict, timestamp_live: float, timestamp_lake: float, timestamp_rain: float):
        val_to_pdk = {}
        #val_to_pdk[last_vals["live"]] = PDK_GASES
        val_to_pdk[last_vals["lake"]] = PDK_LAKE
        val_to_pdk[last_vals["rain"]] = PDK_RAIN
        self.pdkClass = PdkClass(val_to_pdk)
        self.uid = uid
        self.lat = lat
        self.lon = lon
        self.timestamp_live = timestamp_live
        self.timestamp_lake = timestamp_lake
        self.timestamp_rain = timestamp_rain

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