from bson import ObjectId


def is_valid_objectid(id: str):

    return ObjectId.is_valid(id)