from flask import Flask, request, make_response, render_template_string
import json
import pymongo as mongo
import datetime as dt
import threading as thrd
from websockets.client import WebSocketClientProtocol

import utility as u
import calc as c
import wsserver as wss

app = Flask(__name__)

app.db = mongo.MongoClient("mongodb://localhost:27017").siburopenecomap

wsserver = wss.Server(app.db)

LIVE_PARAMS = [
    "temp", "tempSpeed",
    "humidity", "humiditySpeed",
    "light", "lightSpeed",
    "gas", "gasSpeed"
]

LIVE_PARAMS_DEVICED = [
    "temp",
    "humidity",
    "light",
    "gas"
]

c.fund.init(app.db, LIVE_PARAMS)

@app.route("/")
def index():
    return "SiburOpenEcoMap is running!"

"""
Update values - internal api
/devicelive/<uid: string>/<params: string>
url parameters:
    uid: UID of device
    params: in format - <param>-<value>_<param>-<value>_<param>-<value>
parametrs:
    con - any - any - optional - if exists, device confirms that it recieved information about probe
headers:
    Token: <uid> <utoken> - secret token for each device

resp:
    //not json format
    pong: pong - just pong

сохраняет все значения которые передаются в парамс в бд
"""
@app.route("/devicelive/<string:uid>/<string:params>")
def devicelive(uid: str, params: str):
    if not uid: return "empty uid"
    if not params: return "empty param"
    stoken_json = app.db.devices.find_one({"uid": uid})
    if stoken_json: stoken = stoken_json['token']
    else: return "unknown device"
    if not u.need_fields(request.headers, "Token"): return "no Token"
    if not len(request.headers["Token"].split()) == 2: return "invalid auth format"
    if ( not request.headers['Token'].split()[0] == uid ) and ( not request.headers['Token'].split()[1] == stoken ):
        return "auth failed"
    if "con" in request.args.keys():
        stoken_json["is_probe_lake"] = False
        stoken_json["is_probe_rain"] = False
        app.db.devices.find_one_and_replace({"uid": uid}, stoken_json)
    data = {"uid": uid, "timestamp": dt.datetime.now().timestamp()}
    for param in params.split("_"):
        data[param.split("-")[0]] = int(param.split("-")[1])
    for lparam in LIVE_PARAMS_DEVICED:
        if lparam not in data.keys():
            data[lparam] = c.fund.last[data["uid"]][lparam]
    #app.db.liveparams.insert_one(data)
    thrd.Thread(target=c.calc_new_vals, args=(data,)).start()
    return str(int(str(int(stoken_json["is_probe_lake"]))+str(int(stoken_json["is_probe_rain"]))))


"""
Recieve information about probe is ready - internal api
/deviceprobe/<uid: string>/<probe_type: string>
url parameters:
    uid - UID of device - string - required
    probe_type - lake or rain or smthg of ready probe - string - required
headers:
    Token: <uid> <utoken> - secret token for each device - string

resp:
    nu tipo
"""
@app.route("/deviceprobe/<string:uid>/<string:probe_type>")
def deviceprobe(uid: str, probe_type: str):
    if not uid: return "empty uuid"
    if not probe_type: return "empty probe_type"
    if not probe_type in ("lake", "rain"): return "incorrect probe_type"
    device = app.db.devices.find_one({"uid": uid})
    if not device: return "unknown device"
    if not u.need_fields(request.headers, "Token"): return "no Token"
    auth = request.headers["Token"].split()
    if not len(auth) == 2: return "incorrect auth format"
    if ( not auth[0] == device["uid"] ) and ( not auth[1] == device["token"] ): return "auth failed"
    device[f"is_probe_{probe_type}"] = True
    app.db.devices.find_one_and_replace({"uid": uid}, device)
    return "meow"


"""
Get last data for device - external api
/get_last
params:
    uid - UID of device - string - required
    filter - values to be included in the responce (json format) - list[LiveParam] - optional

resp:
    status - ok or err - string <ok or err> - required
    data - dict of information - dict - required:
        ON ERROR:
            reason - information about error - string - required
        ON OK:
            timestemp - timestamp of last measurement - string of datetime in format "YYYY-mm-dd HH:MM:SS" - required
            ll - latitude and longitude of device - dict{...} - required:
                lat - latitued - float - required
                lon - longitude - float - required
            values - dict of LiveParam measurements - dict{LiveParam: value} - required

получает на вход uid устройства и возвращает все (или указанные в фильтре) его последние значения
"""
@app.route("/get_last/")
def get_last():
    if not u.need_fields(request.args, "uid"): return u.return_error("Not enough parametrs")
    if not app.db.devices.find_one({"uid": request.args['uid']}): return u.return_error("Device was not found by this uid")
    if "filter" in request.args.keys():
        try: json.loads(request.args['filter'])
        except Exception: return u.return_error("Filter is not in json format")
        for lparam in json.loads(request.args["filter"]):
            if not lparam in LIVE_PARAMS: return u.return_error(f"Incorrect LiveParam name ({lparam})")
    data = c.fund(request.args["uid"])
    values = {}
    if not "filter" in request.args.keys():
        values = data.copy()
        del values["uid"]
        del values["timestamp"]
    else:
        values = {}
        for liveParam in json.loads(request.args["filter"]):
            values[liveParam] = data[liveParam]
    return u.make_response("ok", {"ll": {"lat": c.fund.ll[request.args["uid"]][0], "lon": c.fund.ll[request.args["uid"]][1]}, "timestamp": data['timestamp'], "values": values})


"""
Get many values for device - external api
/get
params:
    uid - UID of device - string - optional
    timestamp_start - time filter, minimium time value - string of datatime in format "YYYY-mm-dd HH:MM:SS" OR float timestamp in POSIX format - optional
    timestamp_end - time filter, maximium time value - string of datetime in format "YYYY-mm-dd HH:MM:SS" OR float timestamp in POSIX format - optional
    condition - condition filter, for LiveParam - string of condition in format "<LiveParam or int>< < or > or >= or <= or = or != or == ><LiveParam or int> - optional
    filter - values to be included in the response (json format) - list[LiveParam] - optional
    limit - limit of values, to be included in one page, max 250 - int - optional - default value: 25
    page - number of page - int - optional - default value: 1

resp:
    status - ok or err - string <ok or err> - required
    data - dict of information - dict - required:
        ON ERROR:
            reason - information about error - string - required
        ON OK:
            total_items - total count of items found for this request - int - required
            items_on_page - items on this page - int - required
            page - current page - int - required
            pages - pages found for this request - int - required
            values - list of values - list[dict{...}] - required:
                timestamp - timestamp of this measurement - string of timestamp in format "YYYY-mm-dd HH:MM:SS" - required
                uid - UID of device - string - required
                ll - latitude and longitude of device - dict{...} - required:
                    lat - latitued - float - required
                    lon - longitude - float - required
                values - dict of LiveParam measurements - dict{LiveParam: value} - required
"""
@app.route("/get/")
def get__():
    #if not u.need_fields(request.args, "uid"): return u.return_error("Not enough parameters")
    #if not app.db.devices.find_one({"uid": request.args["uid"]}): return u.return_error("Device was not found by this uid")
    if "filter" in request.args.keys():
        try: json.loads(request.args["filter"])
        except Exception: return u.return_error("Filter is not json format")
        for lparam in json.loads(request.args["filter"]):
            if not lparam in LIVE_PARAMS: return u.return_error(f"Incorrect LiveParam name ({lparam})")
    if "timestamp_start" in request.args.keys():
        try: dt.datetime.strptime(request.args["timestamp_start"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            try: float(request.args["timestamp_start"])
            except Exception: return u.return_error("Timestamp (start) in wrong format")
    if "timestamp_end" in request.args.keys():
        try: dt.datetime.strptime(request.args["timestamp_end"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            try: float(request.args["timestamp_end"])
            except Exception: return u.return_error("Timestamp (end) in wrong format")
    condition = None
    if "condition" in request.args.keys():
        conditions = u.parse_condition(request.args['condition'])
        if not conditions[0]: return conditions[1]
        condition = conditions[1]
    if "limit" in request.args.keys():
        try: int(request.args['limit'])
        except Exception: return u.return_error("Argument \"limit\" is not int")
    if "page" in request.args.keys():
        try: int(request.args['page'])
        except Exception: return u.return_error("Argument \"page\" is not int")
    tms_s = u.get_timestamp(request.args["timestamp_start"]) if "timestamp_start" in request.args.keys() else dt.datetime(1990, 7, 13, 12, 0, 0).timestamp()
    tms_e = u.get_timestamp(request.args["timestamp_end"]) if "timestamp_end" in request.args.keys() else dt.datetime(2100, 7, 13, 12, 0, 0).timestamp()
    filter = json.loads(request.args["filter"]) if "filter" in request.args.keys() else None
    resp_values = []
    for data in app.db.data.find():
        resp_values.append({"ll": {"lat": c.fund.ll[data["uid"]][0], "lon": c.fund.ll[data["uid"]][1]}, "uid": data["uid"], "timestamp": data["timestamp"], "values": u.filtered(data, filter)})
        if "uid" in request.args.keys():
            if data["uid"] != request.args["uid"]:
                resp_values.pop()
                continue
        if condition:
            if not u.solve_condiction(condition["sign"],
                                      u.take_live_param_or_int(data, condition["oper1"]),
                                      u.take_live_param_or_int(data, condition["oper2"])):
                resp_values.pop()
                continue
        print(data)
        if not ( data["timestamp"] > tms_s and data["timestamp"] < tms_e ):
            resp_values.pop()
            continue
    limit = int(request.args["limit"]) if "limit" in request.args.keys() else 25
    page = int(request.args["page"]) if "page" in request.args.keys() else 1
    total_pages = (len(resp_values) // limit) + 1
    if page > total_pages: return u.return_error("Page index out of range")
    slic = resp_values[limit*(page-1):limit*page if page != total_pages else (limit*(page-1))+(len(resp_values) % limit)]
    items_on_page = limit if page != total_pages else len(resp_values) % limit
    return u.make_response("ok", {"total_items": len(resp_values), "items_on_page": items_on_page, "page": page,
                                  "pages": total_pages, "values": slic})

"""
Get list of all devices - external api
/devices

resp:
    status - ok or err - string <ok or err> - required
    data - dict of information - dict - required:
        ON ERROR:
            reason - information about error - string - required
        ON OK:
            values - list of dicts with information about devices - list[dict{...}] - required:
                uid - UID of device - string - required
                ll - latitude and longitude of device - dict{...} - required:
                    lat - latitued - float - required
                    lon - longitude - float - required

"""
@app.route("/devices/")
def devices():
    vals = []
    for device in app.db.devices.find():
        valdevice = {}
        valdevice["ll"] = {"lat": c.fund.ll[device["uid"]][0], "lon": c.fund.ll[device["uid"]][1]}
        valdevice["uid"] = device["uid"]
        vals.append(valdevice)
    return u.make_response("ok", {"values": vals})


@c.fund.alertthis()
def make_alert():
    pass


"""
Wbs endpoint for probe uid from drone uid - internal websockets endpoint
op: drone
params (data):
    drone_uid - uid from drone - string - required

resp:
    status - ok or err - string <ok or err> - required
    code - code (more somewhere) - int - required
    ON ERROR:
        info - information about error - string+ - required --- can be a dict with "reason" key and some additional information, on codes: 26
    ON OK:
        info - dict of resp - dict - required:
            probe_uid - uid of probe inside drone - string - required
            probe_type - probe type - string of probe type - required
"""
async def wbs_drone(ws: WebSocketClientProtocol, data: dict):
    if not u.need_fields(data, "drone_uid"):
        await wss.resp(ws, False, "No fields", 24)
        return
    drone = app.db.drones.find_one({"uid": data["drone_uid"]})
    if not drone:
        await wss.resp(ws, False, "Drone doesnot found", 25)
        return
    if drone["taken"]:
        await wss.resp(ws, False, {"reason": "Probe taken", "probe_uid": drone["probe_uid"], "probe_type": drone["probe_type"]}, 26)
        return
    drone["taken"] = True
    app.db.drones.find_one_and_replace({"uid": data["drone_uid"]}, drone)
    await wss.resp(ws, True, {"probe_uid": drone["probe_uid"], "probe_type": drone["probe_type"]}, 10)
wsserver.end_points["drone"] = wbs_drone


"""
Wbs endpoint for read and write data - internal webscokets endpoint
op: super_data
params (data):
    collection - name of collection - string - required
    filter - filter for mongo - dict - optional (required if "replace" provided)
    replace - data to replace this - dict - optional
    insert - data to insert - dict - optional --- if provided filter and replace will not work

resp:
    status - ok or err - string <ok or err> - required
    code - code (more somewhere) - int - required
    ON ERROR:
        info - information about error - string+ - required --- can be a dict with "reason" key and some additional information, on codes: 
    ON OK:
        info - dict of resp - dict - required:
            values - list of values - list[dict] - required
"""
async def wbs_super_data(ws: WebSocketClientProtocol, data: dict):
    if not u.need_fields(data, "collection"):
        await wss.resp(ws, False, "Not enough fields", 24)
        return
    if "replace" in data.keys():
        if not u.need_fields(data, "filter"):
            await wss.resp(ws, False, "Not enough fields", 24)
            return
    coll = app.db.get_collection(data["collection"])
    if len(list(coll.find())) == 0:
        await wss.resp(ws, False, "Failed to find this collection", 27)
        return
    if "insert" in data.keys():
        coll.insert_one(data["insert"])
        vals = coll.find(data["insert"])
        await wss.resp(ws, True, {"values": u.no_id_list(list(vals))}, 10)
        return
    vals = list(coll.find(data["filter"]) if "filter" in data.keys() else coll.find())
    if "replace" in data.keys():
        if len(vals) != 1:
            await wss.resp(ws, False, "Requested filter give more then one or zero values", 28)
            return
        coll.find_one_and_replace(vals[0], data["replace"])
        vals = list(coll.find(data["replace"]))
    await wss.resp(ws, True, {"values": u.no_id_list(vals)}, 10)
wsserver.end_points["super_data"] = wbs_super_data


thrd.Thread(target=wsserver.run_server).start()

app.run("localhost", 1883)