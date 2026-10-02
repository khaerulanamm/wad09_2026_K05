from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.session_controller import router as session_router

app = FastAPI(title="Gym Classes API (MVC)")

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

# Register controller (MVC)
app.include_router(session_router)