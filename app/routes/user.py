from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from passlib.hash import pbkdf2_sha256
from app.auth.auth_handler import sign_jwt
from app.database.user import add_user, retrieve_user
from app.models.user import UserSchema, UserLoginSchema, UserUpdateSchema
from app.models.response import ErrorResponseModel, ResponseModel
from app.auth.auth_bearer import JWTBearer
from bson.objectid import ObjectId
from app.auth.auth_bearer import get_current_user






import logging

from app.database.user import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
)
from app.models.response import (
    ErrorResponseModel,
    ResponseModel,
)
from app.models.user import (
    UserSchema,
    UserLoginSchema
)


router = APIRouter()

async def check_user(data: UserLoginSchema):
    try:
        user = await retrieve_user(data.email)
        if user["email"] == data.email:
            return pbkdf2_sha256.verify(data.password, user['password'])
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=401, detail="Unauthorized : bad credentials") #, headers={"X-error-code": f"Wrong login details!"})
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized : bad credentials" ) #, headers={"X-error-code": f"Wrong password!"})


@router.post("/signup", responses={409: {"description": "User already exists", "model":ErrorResponseModel}})
async def create_user(user: UserSchema = Body(...)):
    user.password = pbkdf2_sha256.hash(user.password)

    try:
        new_user = await add_user(jsonable_encoder(user))
    except Exception as e:
        if e.code == 11000:
            raise HTTPException(status_code=409, detail="User with this email already exists.")
        logging.critical(e)
        raise HTTPException(status_code=400, detail="Unknown error occurred.", headers={"X-error-code": f"{e.code}"})
    return sign_jwt(user.email)

@router.post("/login")
async def user_login(user: UserLoginSchema = Body(...)):
    if await check_user(user):
        return sign_jwt(user.email)

@router.post("/update", dependencies=[Depends(JWTBearer())])
async def user_update(current_user: Annotated[UserSchema, Depends(get_current_user)], user: UserUpdateSchema = Body(...)):
    user.password = pbkdf2_sha256.hash(user.password)
    updated_user = await update_user(current_user["email"], user.model_dump())
    return updated_user


@router.get("/me", dependencies=[Depends(JWTBearer())])
async def read_users_me(current_user: Annotated[UserSchema, Depends(get_current_user)]):
    return current_user