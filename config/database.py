import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

"""
Módulo de configuración y conexión a la base de datos MongoDB.
Incluye carga de variables de entorno, validación y funciones utilitarias.
"""
# =========================================================
# 1. Cargar variables de entorno
# =========================================================
# Detecta si estamos en local o producción
ENV = os.getenv("ENV", "local").lower()

# Carga el .env correspondiente
if ENV == "local":
    load_dotenv(".env.local")
    print("✅ Cargando variables de entorno LOCAL (.env.local)")
else:
    load_dotenv(".env.prod")
    print("✅ Cargando variables de entorno PRODUCCIÓN (.env.prod)")

# =========================================================
# 2. Configuración de MongoDB
# =========================================================
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

if ENV == "local" and not MONGO_URI:
    MONGO_URI = "mongodb://localhost:27017"
    print(f"🔧 Usando MongoDB local por defecto en {MONGO_URI}")

if not MONGO_URI or not MONGO_DB:
    raise RuntimeError("❌ MONGO_URI y/o MONGO_DB no están definidas correctamente.")

# Cliente global
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

# =========================================================
# 3. Validación de variables
# =========================================================
def _validate_env():
    """
    Valida que las variables de entorno necesarias estén definidas.
    Lanza excepción si falta alguna.
    """
    errors = []
    if not MONGO_URI:
        errors.append("MONGO_URI no está definida")
    if not MONGO_DB:
        errors.append("MONGO_DB no está definida")
    if errors:
        raise RuntimeError("; ".join(errors))

# =========================================================
# 4. Inicialización de la BD
# =========================================================
async def init():
    """
    Inicializa la base de datos y crea el índice único en el campo email de la colección users.
    Útil para preparar la base antes de usar la API.
    """
    _validate_env()
    users = db.get_collection("users")
    try:
        result = await users.create_index("email", unique=True)
        print(f"✅ Índice creado: {result}")
    except Exception as e:
        print(f"⚠️ Error creando índice: {e}")
    finally:
        client.close()

# =========================================================
# 5. Conectar y desconectar
# =========================================================
async def connect_to_mongo():
    """
    Establece y devuelve la instancia global de la base de datos MongoDB.
    Lanza excepción si la conexión falla.
    """
    if db is None:
        raise RuntimeError("❌ La conexión a la BD no se inicializó correctamente.")
    print(f"✅ Conexión establecida a MongoDB ({ENV})")
    return db

async def close_mongo_connection():
    """
    Cierra la conexión global a la base de datos MongoDB.
    """
    if client:
        client.close()
        print("🛑 Conexión a MongoDB cerrada.")

# =========================================================
# 6. Ejecución directa para crear índice inicial
# =========================================================
if __name__ == "__main__":
    """
    Permite inicializar la base de datos ejecutando el script directamente.
    Crea el índice único en email.
    """
    try:
        asyncio.run(init())
    except Exception as exc:
        print(f"❌ Fallo al inicializar la base de datos: {exc}")
        raise
