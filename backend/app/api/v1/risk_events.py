from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.risk import RiskEvent, RiskApproval
from app.schemas.risk import (
    RiskEventRead, RiskEventCreate, RiskEventUpdate,
    ApprovalRequestRead, ApprovalRequestCreate, RiskEventPagination
)
from uuid import UUID
import json
import datetime
from datetime import date
from typing import Dict, Any, Optional

from app.core.permissions import PermissionChecker

router = APIRouter()

# --- Helpers ---

def get_next_risk_id(db: Session) -> str:
    # Simple ID generation logic: INC-YYYY-NNN
    # In production, use sequence or UUID. For now, mimicking mock: INC-2024-NNN
    # Query last ID
    year = datetime.datetime.now().year
    prefix = f"INC-{year}-"
    
    last = db.query(RiskEvent).filter(RiskEvent.id.like(f"{prefix}%")).order_by(desc(RiskEvent.id)).first()
    if not last:
        return f"{prefix}001"
    
    try:
        num_part = int(last.id.split('-')[-1])
        new_num = num_part + 1
        return f"{prefix}{new_num:03d}"
    except Exception:
        return f"{prefix}001"

def get_next_req_id(db: Session) -> str:
    # REQ-NNN
    last = db.query(RiskApproval).order_by(desc(RiskApproval.id)).first()
    if not last:
        return "REQ-001"
    
    try:
        # Assuming REQ-NNN
        if last.id.startswith("REQ-"):
             num_part = int(last.id.split('-')[-1])
             new_num = num_part + 1
             return f"REQ-{new_num:03d}"
        else:
             return "REQ-001"
    except Exception:
        return "REQ-001"

# --- Read Endpoints ---

@router.get("/", response_model=RiskEventPagination)
def list_risk_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    perm: bool = Depends(PermissionChecker("risk_event.read")),
    status: Optional[str] = None,
    severity: Optional[str] = None,
    maker: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    query = db.query(RiskEvent)
    
    if status and status != 'undefined':
        query = query.filter(RiskEvent.status == status)
    if severity and severity != 'undefined':
        query = query.filter(RiskEvent.severity == severity)
    if maker and maker != 'undefined':
        query = query.filter(RiskEvent.maker.ilike(f"%{maker}%"))
    if date_from:
        query = query.filter(RiskEvent.date >= date_from)
    if date_to:
        query = query.filter(RiskEvent.date <= date_to)
        
    # Count total
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    events = query.order_by(RiskEvent.date.desc()).offset(offset).limit(limit).all()
    
    return {
        "items": events,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "limit": limit
    }

@router.get("/approvals/pending", response_model=list[ApprovalRequestRead])
def list_pending_approvals(
    current_user: User = Depends(PermissionChecker("risk_event.approve")),
    db: Session = Depends(get_db)
):
    # Only show pending items. Only Approvers should see this list to act on.
    return db.query(RiskApproval).filter(RiskApproval.status == 'pending').order_by(desc(RiskApproval.timestamp)).all()

@router.get("/requests/mine", response_model=list[ApprovalRequestRead])
def list_my_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Show all requests made by the current user (status: pending, approved, rejected)
    return db.query(RiskApproval).filter(RiskApproval.requested_by_id == current_user.id).order_by(desc(RiskApproval.timestamp)).all()

# --- Mutation Request Endpoint (Maker) ---

@router.post("/request", response_model=ApprovalRequestRead)
def create_request(
    request_in: ApprovalRequestCreate,
    current_user: User = Depends(PermissionChecker("risk_event.create")),
    db: Session = Depends(get_db)
):
    # Depending on roles, we might restrict who can create requests. 
    # For now, any auth user can be a Maker.
    
    new_id = get_next_req_id(db)
    
    approval = RiskApproval(
        id=new_id,
        action=request_in.action,
        status='pending',
        payload=request_in.payload,
        target_incident_id=request_in.target_incident_id,
        requested_by_id=current_user.id,
        note=request_in.note
    )
    
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval

# --- Approval Action Endpoint (Checker) ---

@router.post("/approvals/{req_id}/{action}")
def process_approval(
    req_id: str,
    action: str, # approve / reject
    current_user: User = Depends(PermissionChecker("risk_event.approve")),
    db: Session = Depends(get_db)
):
    # Checker role implementation:
    # Ideally, Maker cannot Approve their own request.
    
    req = db.query(RiskApproval).filter(RiskApproval.id == req_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
        
    if req.status != 'pending':
         raise HTTPException(status_code=400, detail=f"Request already processed: {req.status}")

    # Prevent Self-Approval (Maker-Checker Rule)
    # if req.requested_by_id == current_user.id:
    #      raise HTTPException(status_code=403, detail="Maker cannot approve their own request")

    if action not in ['approve', 'reject']:
        raise HTTPException(status_code=400, detail="Invalid action")
        
    req.status = 'approved' if action == 'approve' else 'rejected'
    req.assessed_by_id = current_user.id
    
    if action == 'approve':
        try:
            if req.action == 'create':
                # Create the Risk Event
                data = req.payload
                new_event_id = get_next_risk_id(db)
                
                # Fetch requester username for 'maker' field
                maker_user = db.query(User).filter(User.id == req.requested_by_id).first()
                maker_name = maker_user.username if maker_user else "Unknown"
                
                new_event = RiskEvent(
                    id=new_event_id,
                    report_title=data.get('reportTitle'),
                    client_code=data.get('clientCode'),
                    risk_description=data.get('riskDescription'),
                    severity=data.get('severity'),
                    impact=data.get('impact'),
                    action_taken=data.get('actionTaken'),
                    follow_up_plan=data.get('followUpPlan'),
                    additional_notes=data.get('additionalNotes'),
                    images=data.get('images', []),
                    status='Published', # Status matches Frontend type
                    date=data.get('date'),
                    time=datetime.datetime.now().strftime("%H:%M"),
                    maker=maker_name,
                    approver=current_user.username,
                    created_by_id=req.requested_by_id,
                    approved_by_id=current_user.id
                )
                db.add(new_event)
                # Update target ID in the request so we can link it later if needed
                req.target_incident_id = new_event_id
                
            elif req.action == 'edit':
                event = db.query(RiskEvent).filter(RiskEvent.id == req.target_incident_id).first()
                if event:
                    data = req.payload
                    # Update fields
                    event.report_title = data.get('reportTitle', event.report_title)
                    event.client_code = data.get('clientCode', event.client_code)
                    event.risk_description = data.get('riskDescription', event.risk_description)
                    event.severity = data.get('severity', event.severity)
                    event.impact = data.get('impact', event.impact)
                    event.action_taken = data.get('actionTaken', event.action_taken)
                    event.follow_up_plan = data.get('followUpPlan', event.follow_up_plan)
                    event.additional_notes = data.get('additionalNotes', event.additional_notes)
                    event.images = data.get('images', event.images)
                    event.date = data.get('date', event.date)
                    
                    event.updated_at = datetime.datetime.now()
                    # We might update 'maker' to the editor, or keep original?
                    # Usually audit trail keeps 'Last Modified By'. 
                    # For simple 'maker' field, let's leave it or append?
                    # Let's simple update not change 'maker' but maybe we need 'last_editor'
                    
            elif req.action == 'delete':
                event = db.query(RiskEvent).filter(RiskEvent.id == req.target_incident_id).first()
                if event:
                    db.delete(event)
                    
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to apply changes: {str(e)}")
            
    db.commit()
    return {"message": f"Request {action}d successfully"}
