from pydantic import BaseModel, Field, EmailStr


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(primary_key=True, example="fred@test.be", description="User\'s Email (must be unique)")
    password: str = Field(..., example="weakpassword")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "email@example.com",
                "password": "weakpassword"
            }
        }

class UserSchema(UserLoginSchema):
    fullname: str = Field(..., example="Full Name")

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Full Name",
                "email": "email@example.com",
                "password": "weakpassword"
            }
        }

class UserUpdateSchema(BaseModel):
    fullname: str = Field(..., example="Full Name")
    password: str = Field(..., example="newpassword")
    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Full Name",
                "password": "newpassword"
            }
        }