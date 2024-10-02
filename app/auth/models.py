from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Zhumaev Rakhat",
                "email": "zhumaevrakhat@gmail.com",
                "password": "example_password",
            }
        }
