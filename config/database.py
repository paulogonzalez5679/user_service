import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv, find_dotenv

# Busca el archivo .env en el árbol de directorios y lo carga si existe.
dotenv_path = find_dotenv(usecwd=True)
if dotenv_path:
    load_dotenv(dotenv_path)
    print(f"Cargando variables de entorno desde: {dotenv_path}")
else:
    # Si no hay .env, intentamos cargar .env.example como fallback
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_example = os.path.join(project_root, ".env.example")
    if os.path.exists(env_example):
        load_dotenv(env_example)
        print(f"No se encontró .env; cargando variables desde: {env_example}")
    else:
        # Intentamos carga por defecto para mantener compatibilidad
        load_dotenv()
        print("No se encontró .env ni .env.example; se intentó carga por defecto (si existe .env en cwd).")

# Lee y valida variables necesarias

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

if not MONGO_URI or not MONGO_DB:
    raise RuntimeError("MONGO_URI y/o MONGO_DB no están definidas en las variables de entorno")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

def _validate_env():
    errors = []
    if not MONGO_URI:
        errors.append("MONGO_URI no está definida")
    if not MONGO_DB:
        errors.append("MONGO_DB no está definida")
    if errors:
        raise RuntimeError("; ".join(errors))

async def init():
    """Inicializa la BD: crea colección 'users' y un índice único en 'email'."""
    _validate_env()
    if MONGO_DB is None:
        raise RuntimeError("MONGO_DB no está definida")
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]
    users = db.get_collection("users")
    try:
        result = await users.create_index("email", unique=True)
        print("Índice creado:", result)
    except Exception as e:
        print("Error creando índice:", e)
    finally:
        client.close()

# ----------------------------------------------------
# 1. Función para CONECTAR (devuelve el objeto db)
# ----------------------------------------------------
async def connect_to_mongo():
    """Devuelve la instancia global de la base de datos."""
    if db is None:
        raise RuntimeError("La conexión a la BD no se inicializó correctamente.")
    print("Conexión a MongoDB establecida.")
    return db

# ----------------------------------------------------
# 2. Función para CERRAR la conexión
# ----------------------------------------------------
async def close_mongo_connection():
    """Cierra la conexión a la base de datos."""
    if client:
        client.close()
        print("Conexión a MongoDB cerrada.")


if __name__ == "__main__":
    try:
        asyncio.run(init())
    except Exception as exc:
        print("Fallo al inicializar la base de datos:", exc)
        raise
