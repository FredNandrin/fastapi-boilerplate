from pydantic import BaseModel, Field

def ResponseModel(data:dict, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error:str, code: int, message:str):
    return {"error": error, "code": code, "message": message}