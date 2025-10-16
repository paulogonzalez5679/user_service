from fastapi import FastAPI, Request
from routes.user_routes import router as user_router
from config.database import connect_to_mongo, close_mongo_connection
from dotenv import load_dotenv
import os
import time
import uvicorn

# Cargar variables de entorno desde el archivo .env (si existe)
load_dotenv()

# Obtener configuración
PORT = int(os.getenv("PORT", 8000))
ENV = os.getenv("ENV", "local")  # Puede ser local, production, railway, etc.

app = FastAPI(
    title="user_service",
    version="1.0.0",
    description=f"Running in {ENV} environment"
)

# ==========================
# EVENTOS DE INICIO Y CIERRE
# ==========================
@app.on_event("startup")
async def startup_event():
    print(f"🚀 Iniciando aplicación en entorno: {ENV}")
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# ==========================
# MIDDLEWARE DE LOGS
# ==========================
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    print(f"[{request.method}] {request.url.path} completed in {process_time:.2f}ms")
    response.headers["X-Process-Time-ms"] = f"{process_time:.2f}"
    return response

# ==========================
# ROUTES
# ==========================
app.include_router(user_router, prefix="/users", tags=["users"])

# ==========================
# RUN SERVER
# ==========================
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=(ENV == "local"))
