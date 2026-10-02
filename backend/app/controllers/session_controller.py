from fastapi import APIRouter, HTTPException, status, Response
from app.data import SESSIONS
from app.models.session import SessionIn, SessionOut

router = APIRouter(prefix="/sessions", tags=["sessions"])

def get_next_id():
    if not SESSIONS:
        return 1
    return max(session["id"] for session in SESSIONS) + 1

@router.post("", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def create_session(session_in: SessionIn):
    # Validasi Pydantic sudah tertangani otomatis oleh SessionIn
    new_session = session_in.model_dump()
    # Konversi dt.date menjadi string ISO agar konsisten
    new_session["date"] = new_session["date"].isoformat()

    for session in SESSIONS:
        if (
            session["instructor"] == new_session["instructor"]
            and session["date"] == new_session["date"]
            and session["start_time"] == new_session["start_time"]
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Instruktur sudah mengajar kelas lain pada tanggal dan jam yang sama",
            )

    new_session["id"] = get_next_id()
    SESSIONS.append(new_session)
    return new_session

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(id: int):
    for index, session in enumerate(SESSIONS):
        if session["id"] == id:
            SESSIONS.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
