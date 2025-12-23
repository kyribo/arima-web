from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings
from app.models.user import User
from app.models.session import Session as UserSession
from app.models.user_secret import UserSecret
from app.schemas.token import Token
from datetime import timedelta, datetime, timezone
import secrets
import pyotp

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    otp: str | None = Form(None),
    db: Session = Depends(get_db)
):
    # Determine if login is by email or username (form_data.username can be either)
    # The frontend usually sends 'username' field, but user might type email
    user = db.query(User).filter(
        (User.email == form_data.username) | (User.username == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # 2FA Check
    if user.is_2fa_enabled:
        if not otp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="2FA code required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify OTP
        user_secret = db.query(UserSecret).filter(UserSecret.user_id == user.id).first()
        if not user_secret or not user_secret.totp_secret:
             # Should not happen if is_2fa_enabled is true, but fail safe
             raise HTTPException(status_code=400, detail="2FA configuration error")
             
        totp = pyotp.TOTP(user_secret.totp_secret)
        if not totp.verify(otp, valid_window=1):
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid 2FA code",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create Session
    refresh_token = secrets.token_urlsafe(32)
    user_agent = request.headers.get("user-agent")
    client_host = request.client.host if request.client else None
    
    new_session = UserSession(
        user_id=user.id,
        refresh_token=refresh_token,
        user_agent=user_agent,
        ip_address=client_host,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7) # 7 days refresh token
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session) # Get ID

    access_token = create_access_token(
        subject=user.username, 
        expires_delta=access_token_expires,
        session_id=str(new_session.id)
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "refresh_token": refresh_token 
    }

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.core.security import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        session_id: str = payload.get("sid")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
        
    # Attach current session ID to user instance for downstream usage
    user.current_session_id = session_id
    
    return user
