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
Get data for device - external api
/get
params:
    uid - UID of device - string - required
    filter - values to be included in the responce (json format) - list[LiveParam] - optional

resp:
    status - ok or err - string one of ["ok", "err"] - required
    data - dict of information - dict - required:
        ON ERROR:
            reason - information about error - string - required
        ON OK:
            timestemp - timestamp of last measurement - string of datetime in format "YYYY-mm-dd HH:MM:SS" - required
            values - dict of LiveParam measurements - dict{LiveParam: value} - required

получает на вход uid устройства и возвращает все (или указанные в фильтре) его последние значения
"""
@app.route("/get/")
def get():
    if not u.need_fields(request.args, "uid"): return u.return_error("Not enough parametrs")
    if not app.db.devices.find_one({"uid": request.args['uid']}): return u.return_error("Device was not found by this uid")
    #представьте еррор на неправильное название фильтра
    data = app.db.data.find_one({"timestamp": c.fund.last_timestamps[request.args['uid']], "uid": request.args['uid']})
    if not data: u.return_error("Last record was not found for this device") #да я буду перепроверять вручную, не через fund
    values = data.copy()
    del values["_id"]
    del values["uid"]
    del values["timestamp"]
    values["temperatureSpeed"] = c.fund(request.args["uid"])
    return u.make_response("ok", {"timestamp": data['timestamp'], "values": values})

app.run("localhost", 183)