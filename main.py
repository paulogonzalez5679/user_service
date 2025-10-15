from fastapi import FastAPI
from routes.user_routes import router as user_router
from config.database import connect_to_mongo, close_mongo_connection
import time
from fastapi import Request


app = FastAPI(title="user_service", version="1.0.0")


# Conexiones DB
@app.on_event("startup")
async def startup_event():
	await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
	await close_mongo_connection()


# Middleware 
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
	start_time = time.perf_counter()
	response = await call_next(request)
	process_time = (time.perf_counter() - start_time) * 1000
	print(f"[{request.method}] {request.url.path} completed in {process_time:.2f}ms")
	response.headers["X-Process-Time-ms"] = f"{process_time:.2f}"
	return response


app.include_router(user_router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)