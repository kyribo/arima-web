from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.session import Session as SessionModel
from app.schemas.session import SessionRead

router = APIRouter()

@router.get("/", response_model=List[SessionRead])
def get_user_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sessions = db.query(SessionModel).filter(
        SessionModel.user_id == current_user.id,
        SessionModel.is_revoked == False
    ).order_by(SessionModel.last_active_at.desc()).all()
    
    # Check current session
    current_sid = getattr(current_user, "current_session_id", None)
    
    # Convert to schema compatible list (Pydantic models from ORM)
    # We can't just modify ORM objects in place easily for non-column attributes without setup, 
    # but we can return Pydantic models directly if configured.
    # However, since we defined is_current in Schema but it's not in DB, we need to calculate it.
    
    result = []
    for s in sessions:
        # Create Pydantic model
        s_data = SessionRead.model_validate(s)
        s_data.is_current = (str(s.id) == str(current_sid)) if current_sid else False
        result.append(s_data)
        
    return result

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    session.is_revoked = True
    db.commit()
    return None
