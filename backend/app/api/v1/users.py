from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate, UserCreate
from uuid import UUID

router = APIRouter()

# --- Admin Routes ---

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserRead)
def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Reuse the generic update logic or keep distinct
    return update_user(current_user.id, user_update, current_user, db)

@router.get("/", response_model=list[UserRead])
def list_users(
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check permissions (basic role check for now)
    if current_user.role not in ['Superadmin', 'Admin']:
         raise HTTPException(status_code=403, detail="Not authorized")

    query = db.query(User)
    
    if search:
        search_filter = or_(
            User.username.ilike(f"%{search}%"),
            User.email.ilike(f"%{search}%"),
            User.first_name.ilike(f"%{search}%"),
            User.last_name.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
        
    users = query.offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=UserRead)
def create_user(
    user_in: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ['Superadmin', 'Admin']:
         raise HTTPException(status_code=403, detail="Not authorized")
         
    # Check if user exists
    if db.query(User).filter((User.email == user_in.email) | (User.username == user_in.username)).first():
        raise HTTPException(status_code=400, detail="Username or email already exists")
        
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        role=user_in.role,
        access=user_in.access,
        is_active=user_in.is_active,
        phone=user_in.phone,
        bio=user_in.bio,
        location=user_in.location,
        avatar_url=user_in.avatar_url
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Allow users to read their own profile, otherwise admin check
    if current_user.id != user_id and current_user.role not in ['Superadmin', 'Admin']:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Permission check: Users can update themselves (restricted fields), Admins can update anyone
    is_admin = current_user.role in ['Superadmin', 'Admin']
    if not is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Restrict non-admins from changing role/access/active status
    if not is_admin:
        update_data.pop('role', None)
        update_data.pop('access', None)
        update_data.pop('is_active', None)
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ['Superadmin', 'Admin']:
         raise HTTPException(status_code=403, detail="Not authorized")
         
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    db.delete(user)
    db.commit()

# --- Me Routes (kept for compatibility) ---


