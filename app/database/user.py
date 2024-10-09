from bson.objectid import ObjectId
import motor.motor_asyncio
import os
from decouple import config
import logging
from fastapi.encoders import jsonable_encoder
from app.models.user import UserSchema
from fastapi import HTTPException


MONGO_DETAILS = "mongodb://root:password@localhost:27017"; # config('MONGO_DATABASE')

database = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS).myapi

user_collection = database.get_collection("user_collection")

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
        "password": user["password"]
    }

# Retrieve all users present in the database
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user into to the d
async def add_user(user_data: dict) -> dict:
    user_data["_id"]=user_data["email"]
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Retrieve a user with a matching ID
async def retrieve_user(email: str) -> UserSchema:
    user = await user_collection.find_one({"email": email})
    if user:
        return user_helper(user)
    raise HTTPException(status_code=404, detail="not found")


# Update a user with a matching ID
async def update_user(email: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"email": email})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": (user["_id"])}, {"$set": data}
        )
        if updated_user:
            return await retrieve_user(email)
        return HTTPException(status_code=400, detail="error updating user")
    return HTTPException(status_code=404, detail="User not found")


# Delete a user from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True