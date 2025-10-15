from fastapi import APIRouter, HTTPException, status, Depends
from models.user import UserCreate, UserResponse, UserUpdate, UserInDB
from config import database
from passlib.context import CryptContext
from bson import ObjectId


router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
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
	return database.db.get_collection("users")


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
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
    coll = await get_collection()
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")
    user = await coll.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
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
    coll = await get_collection()
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")
    res = await coll.delete_one({"_id": ObjectId(user_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return None