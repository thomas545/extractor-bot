def responsify(data, status_code=200):
    return {"data": data, "status": "success", "status_code": status_code}
