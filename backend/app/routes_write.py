"""B3 dan B4: menambah dan menghapus sesi."""

from itertools import count

from fastapi import APIRouter, HTTPException, Response, status

from app.data import SESSIONS
from app.schemas import SessionIn, SessionOut

router = APIRouter(prefix="/sessions", tags=["sessions"])

# Penghitung id terpisah, supaya id yang sudah dihapus tidak pernah dipakai ulang.
_next_id = count(max((s["id"] for s in SESSIONS), default=0) + 1)


@router.post("", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def create_session(payload: SessionIn):
    data = payload.model_dump(mode="json")
    bentrok = any(
        s["instructor"].lower() == data["instructor"].lower()
        and s["date"] == data["date"]
        and s["start_time"] == data["start_time"]
        for s in SESSIONS
    )
    if bentrok:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Instruktur ini sudah punya kelas pada tanggal dan jam yang sama.",
        )
    session = {"id": next(_next_id), **data}
    SESSIONS.append(session)
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int):
    for index, s in enumerate(SESSIONS):
        if s["id"] == session_id:
            SESSIONS.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Session not found")
