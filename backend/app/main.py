import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes_read import router as read_router
from app.routes_write import router as write_router

app = FastAPI(title="Jadwal Kelas Gym API")

# B5: hanya origin frontend yang boleh memanggil API dari browser, bukan "*".
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(read_router)
app.include_router(write_router)
