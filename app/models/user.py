from pydantic import BaseModel, Field, EmailStr,ConfigDict


class UserLoginSchema(BaseModel):
    model_config = ConfigDict(
        json_schema_extra = {
            "primary_key":True,
            "example": {
                "email": "email@example.com",
                "password": "weakpassword"
            }
        }
    )
    email: EmailStr = Field( examples=["fred@test.be"], description="User\'s Email (must be unique)")
    password: str = Field(..., examples=["weakpassword"])

   
    

class UserSchema(UserLoginSchema):
    model_config = ConfigDict(json_schema_extra = {
            "example": {
                "fullname": "Full Name",
                "email": "email@example.com",
                "password": "weakpassword"
            }
        }
    )
    fullname: str = Field(..., examples=["Full Name"])

class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(json_schema_extra = {
            "example": {
                "fullname": "Full Name",
                "password": "newpassword"
            }
        }) 
    fullname: str = Field(..., examples=["Full Name"])
    password: str = Field(..., examples=["newpassword"])
        