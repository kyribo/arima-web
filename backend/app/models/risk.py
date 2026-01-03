from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from app.core.database import Base

class RiskEvent(Base):
    __tablename__ = "risk_events"
    __table_args__ = {"schema": "riske"}

    id = Column(String, primary_key=True) # Using String ID (e.g., INC-2024-001) as per existing requirement, or UUID?
    # Based on mock data 'INC-2024-004', let's stick to String.
    
    report_title = Column(String, nullable=False)
    client_code = Column(String, nullable=False)
    risk_description = Column(Text, nullable=False)
    severity = Column(String, nullable=False) # low, medium, high, critical
    impact = Column(Text)
    action_taken = Column(Text)
    follow_up_plan = Column(Text)
    additional_notes = Column(Text)
    images = Column(JSONB, default=[]) # List of image URLs
    status = Column(String, nullable=False) # Waiting for Approval, Open, In Progress, Resolved, Closed
    
    date = Column(String, nullable=False) # YYYY-MM-DD
    time = Column(String) # HH:MM
    
    # Audit
    maker = Column(String) # Username/Name of maker
    approver = Column(String) # Username/Name of approver
    
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"))
    approved_by_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)

class RiskApproval(Base):
    __tablename__ = "risk_approvals"
    __table_args__ = {"schema": "riske"}

    id = Column(String, primary_key=True) # REQ-XXX
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    action = Column(String, nullable=False) # create, edit, delete
    status = Column(String, default="pending") # pending, approved, rejected
    
    payload = Column(JSONB, default={}) # Snapshot of data for create/edit
    target_incident_id = Column(String, nullable=True) # Linked Incident ID
    
    requested_by_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"))
    assessed_by_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=True)
    
    note = Column(Text)
    
    # Relationships for easier access
    requester = relationship("User", foreign_keys=[requested_by_id])
    assessor = relationship("User", foreign_keys=[assessed_by_id])
