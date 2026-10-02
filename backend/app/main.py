from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.session_controller import router as session_router

from app.controllers.session_read_controller import router as session_read_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Bagian B: Konfigurasi CORS hanya untuk origin frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route contoh bawaan
@app.get("/health")
def read_health():
    return {"Health": "OK"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


# Bagian A: daftar dan detail sesi (B1, B2)
app.include_router(session_read_router)
