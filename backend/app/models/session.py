from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Session(Base):
    __tablename__ = "sessions"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id", ondelete="CASCADE"), nullable=False)
    refresh_token = Column(String(255), unique=True, nullable=False)
    user_agent = Column(String)
    ip_address = Column(String(45))
    location = Column(String(100))
    is_revoked = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_active_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

    user = relationship("User", back_populates="sessions")
