from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from typing import Optional


class PyObjectId(ObjectId):
	"""
	Validador personalizado para ObjectId de MongoDB en modelos Pydantic.
	Permite validar y serializar ObjectId como string.
	"""
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
	"""
	Modelo base de usuario.
	name: Nombre completo (2-100 caracteres)
	email: Email válido
	"""
	name: str = Field(..., min_length=2, max_length=100)
	email: EmailStr


class UserCreate(UserBase):
	"""
	Modelo para creación de usuario.
	password: Contraseña (mínimo 8 caracteres)
	Ejemplo:
		{
			"name": "Juan Pérez",
			"email": "juan.perez@email.com",
			"password": "MiClaveSegura123"
		}
	"""
	password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
	"""
	Modelo para actualización parcial de usuario.
	Permite modificar nombre, email y/o contraseña.
	"""
	name: Optional[str] = Field(None, min_length=2, max_length=100)
	email: Optional[EmailStr] = None
	password: Optional[str] = Field(None, min_length=8)


class UserInDB(UserBase):
	"""
	Modelo de usuario almacenado en la base de datos.
	Incluye id y contraseña hasheada.
	"""
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	hashed_password: str


class Config:
	"""
	Configuración para serialización de modelos con ObjectId.
	"""
	allow_population_by_field_name = True
	json_encoders = {ObjectId: str}


class UserResponse(UserBase):
	"""
	Modelo de respuesta para usuario (API).
	Incluye id como string.
	"""
	id: str
