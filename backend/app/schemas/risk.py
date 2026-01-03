from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

# --- Risk Event Schemas ---

class RiskEventBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    report_title: str
    client_code: str
    risk_description: str
    severity: str
    impact: Optional[str] = None
    action_taken: Optional[str] = None
    follow_up_plan: Optional[str] = None
    additional_notes: Optional[str] = None
    images: List[str] = []
    status: str
    date: str
    time: Optional[str] = None

class RiskEventCreate(RiskEventBase):
    pass # Created via approval request primarily, but schema needed for validation

class RiskEventUpdate(BaseModel):
    report_title: Optional[str] = None
    client_code: Optional[str] = None
    risk_description: Optional[str] = None
    severity: Optional[str] = None
    impact: Optional[str] = None
    action_taken: Optional[str] = None
    follow_up_plan: Optional[str] = None
    additional_notes: Optional[str] = None
    images: Optional[List[str]] = None
    status: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

class RiskEventRead(RiskEventBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    maker: Optional[str] = None
    approver: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None

class RiskEventPagination(BaseModel):
    items: List[RiskEventRead]
    total: int
    page: int
    pages: int
    limit: int

# --- Approval Schemas ---

class ApprovalRequestBase(BaseModel):
    action: str # create, edit, delete
    target_incident_id: Optional[str] = None
    payload: Dict[str, Any] = {}
    note: Optional[str] = None

class ApprovalRequestCreate(ApprovalRequestBase):
    pass

class ApprovalRequestRead(ApprovalRequestBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    status: str
    timestamp: datetime
    requested_by_id: UUID
    assessed_by_id: Optional[UUID] = None
