from flask import Flask, request, make_response, render_template_string
import json
import pymongo as mongo
import datetime as dt
import threading as thrd

import utility as u
import calc as c

app = Flask(__name__)

app.db = mongo.MongoClient("mongodb://localhost:27017").siburopenecomap

@app.route("/")
def index():
    return "SiburOpenEcoMap is running!"

"""
Update values - internal api
/device/<uid: string>/<params: string>
url parameters:
    id: UID of device
    params: in format - <param>-<value>_<param>-<value>_<param>-<value>
headers:
    Token: <uid> <utoken> - secret token for each device

resp:
    //not json format
    pong: pong - just pong

сохраняет все значения которые передаются в парамс в бд
"""
@app.route("/device/<string:uid>/<string:params>")
def device(uid: str, params: str):
    if not uid: return "empty uid"
    stoken_json = app.db.devices.find_one({"uid": uid})
    print(uid)
    print(stoken_json)
    if stoken_json: stoken = stoken_json['token']
    else: return "unknown device"
    print(request.headers)
    if not u.need_fields(request.headers, "Token"): return "no token"
    if not len(request.headers["Token"].split()) == 2: return "invalid auth format"
    if ( not request.headers['Token'].split()[0] == uid ) and ( not request.headers['Token'].split()[1] == stoken ):
        return "auth failed"
    data = {"uid": uid, "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    for param in params.split("_"):
        data[param.split("-")[0]] = param.split("-")[1]
    app.db.data.insert_one(data)
    thrd.Thread(target=c.calc_new_vals, args=(data,)).start()
    return "pong"


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
    #представьте еррор на неправильное название фильтра
    data = app.db.data.find_one({"timestamp": c.fund.last_timestamps[request.args['uid']], "uid": request.args['uid']})
    if not data: u.return_error("Last record was not found for this device") #да я буду перепроверять вручную, не через fund
    values = {}
    if not "filter" in request.args.keys():
        values = data.copy()
        del values["_id"]
        del values["uid"]
        del values["timestamp"]
        values["temperatureSpeed"] = c.fund(request.args["uid"])
    else:
        d = data.copy()
        values = {}
        for liveParam in json.loads(request.args["filter"]):
            values[liveParam] = d[liveParam]
    return u.make_response("ok", {"timestamp": data['timestamp'], "values": values})


"""
Get many values for device - external api
/get
params:
    uid - UID of device - string - required
    timestamp_start - time filter, minimium time value - string of datatime in format "YYYY-mm-dd HH:MM:SS" - optional
    timestamp_end - time filter, maximium time value - string of datetime in format "YYYY-mm-dd HH:MM:SS" - optional
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
                values - dict of LiveParam measurements - dict{LiveParam: value} - required
"""
@app.route("/get")
def get():
    if not u.need_fields(request.args, "uid"): return u.return_error("Not enough parameters")
    if not app.db.devices.find_one({"uid": request.args["uid"]}): return u.return_error("Device was not found by this uid")
    if "filter" in request.args.keys():
        try: json.loads(request.args["filter"])
        except Exception: return u.return_error("Filter is not json format")
    if "timestamp_start" in request.args.keys():
        try: dt.datetime.strptime(request.args["timestamp_start"], "%Y-%m-%d %H:%M:%S")
        except Exception: return u.return_error("Timestamp (start) in wrong format")
    if "timestamp_end" in request.args.keys():
        try: dt.datetime.strptime(request.args["timestamp_end"], "%Y-%m-%d %H:%M:%S")
        except Exception: return u.return_error("Timestamp (end) in wrong format")
    if "condition" in request.args.keys():
        cond = request.args['condition']
        if ">" in cond:
            if not cond.split(">") == 2: return u.return_error("Condition parse failed (Not two operands)")
            try: int(cond.split(">")[0])
            except Exception:
                #проверка на фильтр
                pass
            try: int(cond.split(">")[1])
            except Exception:
                #проверка на фильтр
                pass
        elif "<" in cond:
            if not cond.split("<") == 2: return u.return_error("Condition parse failed (Not two operands)")
            try: int(cond.split("<")[0])
            except Exception:
                #проверка на фильтр
                pass
            try: int(cond.split("<")[1])
            except Exception:
                #проверка на фильтр
                pass
        elif ">=" in cond:
            if not cond.split(">=") == 2: return u.return_error("Condition parse failed (Not two operands)")
            try: int(cond.split(">=")[0])
            except Exception:
                #проверка на фильтр
                pass
            try: int(cond.split(">=")[1])
            except Exception:
                #проверка на фильтр
                pass
        elif "<=" in cond:
            if not cond.split("<=") == 2: return u.return_error("Condition parse failed (Not two operands)")
            try: int(cond.split("<=")[0])
            except Exception:
                #проверка на фильтр
                pass
            try: int(cond.split("<=")[1])
            except Exception:
                #проверка на фильтр
                pass
        elif "==" in cond:
            if not cond.split("==") == 2: return u.return_error("Condition parse failed (Not two operands)")
            try: int(cond.split("==")[0])
            except Exception:
                #проверка на фильтр
                pass
            try: int(cond.split("==")[1])
            except Exception:
                #проверка на фильтр
                pass
        elif "!=" in cond:
            if not cond.split("!=") == 2: return u.return_error("Condition parse failed (Not two operands)")
            try: int(cond.split("!=")[0])
            except Exception:
                #проверка на фильтр
                pass
            try: int(cond.split("!=")[1])
            except Exception:
                #проверка на фильтр
                pass
        elif "=" in cond:
            if not cond.split("=") == 2: return u.return_error("Condition parse failed (Not two operands)")
            try: int(cond.split("=")[0])
            except Exception:
                #проверка на фильтр
                pass
            try: int(cond.split("=")[1])
            except Exception:
                #проверка на фильтр
                pass
        else: u.return_error("Condition parse failed (No sign detected)")
            
            

app.run("localhost", 183)