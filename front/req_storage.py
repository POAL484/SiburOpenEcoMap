import requests as req
import time

import sdevice

class Storage:
    def __init__(self):
        self.devices = []
    
    def fetch(self):
        new_devices = []
        resp = req.get("http://siburok.ru:1883/devices").json()
        if resp['status'] != "ok":
            print(resp['data']['reason'])
        devices = resp['data']['values']
        #print(devices)
        for device in devices:
            resp = req.get("http://siburok.ru:1883/get_last",
                           params={"uid": device['uid']}).json()
            #print(resp)
            if resp['status'] != "ok":
                print(resp['data']['reason'])
                return
            #print(resp['data'])
            new_devices.append(sdevice.Device.from_responce(device['uid'], resp['data']))
        self.devices = new_devices

    def keep(self):
        time_start = time.time()
        while 1:
            if time.time() - time_start > 13:
                time_start = time.time()
                try: self.fetch()
                except Exception as e: print(f"req_storage fetching error: {e}")
            time.sleep(.33)
