import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.class_controller import router as class_write_router
from app.controllers.class_read_controller import router as class_read_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router


app = FastAPI(title="Jadwal Kelas Gym API")
origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in origins if origin],
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/health")
def read_health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(class_read_router)
app.include_router(class_write_router)
