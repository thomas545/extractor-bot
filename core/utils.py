def covert_object_id_to_str_for_list(objs):
    if objs:
        for obj in objs:
            obj["_id"] = str(obj["_id"])
    return objs
