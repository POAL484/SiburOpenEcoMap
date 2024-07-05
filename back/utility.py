import datetime as dt

def need_fields(obj: dict, *args) -> bool:
    for arg in args:
        if not arg in obj.keys():
            return False
    return True

def make_response(status: str, data: dict):
    return {"status": status, "data": data}

def return_error(reason: str):
    return make_response("err", {"reason": reason})

def parse_condition(cond: str):
    if ">" in cond:
        condition = {"sign": ">"}
        if not cond.split(">") == 2: return (False, "Condition parse failed (Not two operands)")
        try:
            condition["oper1"] = {"type": "int", "val": int(cond.split(">")[0].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper1"] = {"type": "key", "val": cond.split(">")[0].strip()}
        try: 
            condition["oper2"] = {"type": "int", "val": int(cond.split(">")[1].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper2"] = {"type": "key", "val": cond.split(">")[1].strip()}
    elif "<" in cond:
        condition = {"sign": "<"}
        if not cond.split("<") == 2: return (False, "Condition parse failed (Not two operands)")
        try:
            condition["oper1"] = {"type": "int", "val": int(cond.split("<")[0].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper1"] = {"type": "key", "val": cond.split("<")[0].strip()}
        try: 
            condition["oper2"] = {"type": "int", "val": int(cond.split("<")[1].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper2"] = {"type": "key", "val": cond.split("<")[1].strip()}
    elif ">=" in cond:
        condition = {"sign": ">="}
        if not cond.split(">=") == 2: return (False, "Condition parse failed (Not two operands)")
        try:
            condition["oper1"] = {"type": "int", "val": int(cond.split(">=")[0].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper1"] = {"type": "key", "val": cond.split(">=")[0].strip()}
        try: 
            condition["oper2"] = {"type": "int", "val": int(cond.split(">=")[1].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper2"] = {"type": "key", "val": cond.split(">=")[1].strip()}
    elif "<=" in cond:
        condition = {"sign": "<="}
        if not cond.split("<=") == 2: return (False, "Condition parse failed (Not two operands)")
        try:
            condition["oper1"] = {"type": "int", "val": int(cond.split("<=")[0].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper1"] = {"type": "key", "val": cond.split("<=")[0].strip()}
        try: 
            condition["oper2"] = {"type": "int", "val": int(cond.split("<=")[1].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper2"] = {"type": "key", "val": cond.split("<=")[1].strip()}
    elif "==" in cond:
        condition = {"sign": "=="}
        if not cond.split(">") == 2: return (False, "Condition parse failed (Not two operands)")
        try:
            condition["oper1"] = {"type": "int", "val": int(cond.split("==")[0].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper1"] = {"type": "key", "val": cond.split("==")[0].strip()}
        try: 
            condition["oper2"] = {"type": "int", "val": int(cond.split("==")[1].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper2"] = {"type": "key", "val": cond.split("==")[1].strip()}
    elif "!=" in cond:
        condition = {"sign": "!="}
        if not cond.split("!=") == 2: return (False, "Condition parse failed (Not two operands)")
        try:
            condition["oper1"] = {"type": "int", "val": int(cond.split("!=")[0].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper1"] = {"type": "key", "val": cond.split("!=")[0].strip()}
        try: 
            condition["oper2"] = {"type": "int", "val": int(cond.split("!=")[1].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper2"] = {"type": "key", "val": cond.split("!=")[1].strip()}
    elif "=" in cond:
        condition = {"sign": "="}
        if not cond.split("=") == 2: return (False, "Condition parse failed (Not two operands)")
        try:
            condition["oper1"] = {"type": "int", "val": int(cond.split("=")[0].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper1"] = {"type": "key", "val": cond.split("=")[0].strip()}
        try: 
            condition["oper2"] = {"type": "int", "val": int(cond.split("=")[1].strip())}
        except Exception:
            #проверка на фильтр
            condition["oper2"] = {"type": "key", "val": cond.split("=")[1].strip()}
    else: (False, "Condition parse failed (No sign detected)")
    return (True, condition)

def get_timestamp(val: str):
    try: return True, dt.datetime.strptime(val, "%Y-%m-%d %H:%M:%S").timestamp()
    except Exception:
        try: return True, float(val)
        except Exception: return False, None

def solve_condiction(sign: str, oper1: int, oper2: int) -> bool:
    match sign:
        case ">":        return oper1 >  oper2
        case "<":        return oper1 <  oper2
        case ">=":       return oper1 >= oper2
        case "<=":       return oper1 <= oper2
        case "==" | "=": return oper1 == oper2
        case "!=":       return oper1 != oper2
    return False

def take_live_param_or_int(data: dict, operand: dict) -> int:
    if operand["type"] == "int": return int(operand["val"])
    try: return int(data[operand["val"]])
    except KeyError: return 0

def filtered(data: dict, filter: list = None) -> dict:
    if filter:
        d = {}
        for key in filter:
            try: d[key] = data[key]
            except KeyError: pass
        return d
    d = data.copy()
    del d["uid"]
    del d["_id"]
    del d["timestamp"]
    return d