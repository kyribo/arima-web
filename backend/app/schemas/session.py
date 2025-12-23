from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class SessionRead(BaseModel):
    id: UUID
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime
    last_active_at: datetime
    is_revoked: bool
    is_current: bool = False # Helper for frontend

    class Config:
        from_attributes = True
