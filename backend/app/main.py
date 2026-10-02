from fastapi import FastAPI

from app.controllers.session_read_controller import router as session_read_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def read_health():
    return {"Health": "OK"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


# Bagian A: daftar dan detail sesi (B1, B2)
app.include_router(session_read_router)
