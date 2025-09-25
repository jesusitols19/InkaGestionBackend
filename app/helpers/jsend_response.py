def jsend_success(data=None):
    return {"status": "success", "data": data}

def jsend_fail(data=None):
    return {"status": "fail", "data": data}

def jsend_error(message: str, code: int = None, data=None):
    response = {"status": "error", "message": message}
    if code:
        response["code"] = code
    if data:
        response["data"] = data
    return response