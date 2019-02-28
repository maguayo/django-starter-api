
def response_wrapper(success, data, code=None):
	return {"success": success, "code": code, "data": data}
