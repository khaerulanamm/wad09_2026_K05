"""Bagian A (B1, B2): membaca daftar sesi dan satu sesi."""

from fastapi import APIRouter, HTTPException, Query

from app.data import SESSIONS

router = APIRouter(prefix="/sessions", tags=["sessions"])


def find_session(session_id: int) -> dict | None:
    return next((s for s in SESSIONS if s["id"] == session_id), None)


@router.get("")
def list_sessions(
    skip: int = Query(0, ge=0, description="Jumlah baris yang dilewati"),
    limit: int = Query(10, ge=1, le=50, description="Jumlah baris maksimum per halaman"),
    search: str | None = Query(None, max_length=50, description="Cari di nama kelas atau instruktur"),
):
    rows = SESSIONS
    keyword = (search or "").strip().lower()
    if keyword:
        rows = [
            s for s in SESSIONS
            if keyword in s["class_name"].lower() or keyword in s["instructor"].lower()
        ]
    # total dihitung sebelum dipotong, supaya frontend tahu ada berapa halaman.
    return {"items": rows[skip : skip + limit], "total": len(rows), "skip": skip, "limit": limit}


@router.get("/{session_id}")
def get_session(session_id: int):
    session = find_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
