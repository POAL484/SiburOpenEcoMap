

def need_fields(obj: dict, *args) -> bool:
    for arg in args:
        if not arg in obj.keys():
            return False
    return True

def make_response(status: str, data: dict):
    return {"status": status, "data": data}

def return_error(reason: str):
    return make_response("err", {"reason": reason})