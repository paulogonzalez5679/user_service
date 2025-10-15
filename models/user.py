from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from typing import Optional


class PyObjectId(ObjectId):
	@classmethod
	def __get_validators__(cls):
		yield cls.validate

	@classmethod
	def validate(cls, v):
		if not ObjectId.is_valid(v):
			raise ValueError("Invalid ObjectId")
		return ObjectId(v)

	@classmethod
	def __get_pydantic_json_schema__(cls, core_schema, handler):
		return {"type": "string", "title": "ObjectId", "examples": ["507f1f77bcf86cd799439011"]}


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)


class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str


class Config:
    allow_population_by_field_name = True
    json_encoders = {ObjectId: str}


class UserResponse(UserBase):
    id: str
