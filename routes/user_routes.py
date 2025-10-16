from fastapi import APIRouter, HTTPException, status, Depends
from models.user import UserCreate, UserResponse, UserUpdate, UserInDB
from config import database
from passlib.context import CryptContext
from bson import ObjectId


router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Genera el hash seguro de una contraseña usando bcrypt.
    Limita la longitud a 72 bytes y maneja errores de decodificación.
    Args:
        password (str): Contraseña en texto plano.
    Returns:
        str: Contraseña hasheada.
    """
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        while True:
            try:
                password = password_bytes.decode("utf-8")
                break
            except UnicodeDecodeError:
                password_bytes = password_bytes[:-1]
    return pwd_context.hash(password)


async def get_collection():
    """
    Devuelve la colección 'users' de la base de datos MongoDB.
    Returns:
        Collection: Colección de usuarios.
    """
    return database.db.get_collection("users")


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Crea un nuevo usuario en la base de datos.
    - Verifica que el email no esté registrado.
    - Hashea la contraseña antes de guardar.
    Args:
        user (UserCreate): Datos del usuario a crear.
    Returns:
        dict: Usuario creado (id, name, email).
    Ejemplo de uso:
        {
            "name": "Juan Pérez",
            "email": "juan.perez@email.com",
            "password": "MiClaveSegura123"
        }
    """
    coll = await get_collection()
    # Verificacion de email existente
    existing = await coll.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_dict = user.dict()
    user_dict["hashed_password"] = hash_password(user_dict.pop("password"))
    res = await coll.insert_one(user_dict)
    created = await coll.find_one({"_id": res.inserted_id})
    if not created:
        raise HTTPException(status_code=500, detail="User creation failed")
    return {"id": str(created["_id"]), "name": created["name"], "email": created["email"]}


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """
    Obtiene los datos de un usuario por su ID.
    Args:
        user_id (str): ID del usuario (MongoDB ObjectId).
    Returns:
        dict: Usuario encontrado (id, name, email).
    """
    coll = await get_collection()
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")
    user = await coll.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    """
    Actualiza los datos de un usuario existente.
    - Permite cambiar nombre, email y/o contraseña.
    - Verifica unicidad de email.
    Args:
        user_id (str): ID del usuario.
        user_update (UserUpdate): Datos a actualizar.
    Returns:
        dict: Usuario actualizado (id, name, email).
    """
    coll = await get_collection()
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    if "email" in update_data:
        # check uniqueness
        existing = await coll.find_one({"email": update_data["email"], "_id": {"$ne": ObjectId(user_id)}})
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
    result = await coll.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": update_data}, upsert=False, return_document=True)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": str(result["_id"]), "name": result["name"], "email": result["email"]}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """
    Elimina un usuario por su ID.
    Args:
        user_id (str): ID del usuario.
    Returns:
        None
    """
    coll = await get_collection()
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")
    res = await coll.delete_one({"_id": ObjectId(user_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return None