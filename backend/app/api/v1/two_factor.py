from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.models.user_secret import UserSecret
from app.schemas.two_factor import TwoFactorSetupResponse, TwoFactorEnableRequest, TwoFactorVerifyRequest
import pyotp
import qrcode
import io
import base64

router = APIRouter()

@router.post("/setup", response_model=TwoFactorSetupResponse)
def setup_two_factor(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Generate random secret
    secret = pyotp.random_base32()
    
    # Generate Provisioning URI (for QR Code)
    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=current_user.email, 
        issuer_name="Arima Web"
    )
    
    # Generate QR Code Image -> Base64
    img = qrcode.make(uri)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    qr_code_url = f"data:image/png;base64,{img_str}"
    
    # Store secret temporarily or update existing?
    # Better to store in UserSecrets but NOT enable it yet.
    
    user_secret = db.query(UserSecret).filter(UserSecret.user_id == current_user.id).first()
    if not user_secret:
        user_secret = UserSecret(user_id=current_user.id, totp_secret=secret)
        db.add(user_secret)
    else:
        user_secret.totp_secret = secret # Update with new secret
        
    db.commit()
    
    return {"secret": secret, "qr_code_url": qr_code_url}

@router.post("/enable", status_code=status.HTTP_204_NO_CONTENT)
def enable_two_factor(
    payload: TwoFactorEnableRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_secret = db.query(UserSecret).filter(UserSecret.user_id == current_user.id).first()
    if not user_secret or not user_secret.totp_secret:
        raise HTTPException(status_code=400, detail="2FA setup not initiated")
        
    totp = pyotp.TOTP(user_secret.totp_secret)
    if not totp.verify(payload.token, valid_window=1):
        raise HTTPException(status_code=400, detail="Invalid verification code")
        
    # Enable 2FA for user
    current_user.is_2fa_enabled = True
    db.commit()
    return None

@router.post("/disable", status_code=status.HTTP_204_NO_CONTENT)
def disable_two_factor(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.is_2fa_enabled = False
    
    # Optional: Clear secret or keep it? 
    # Usually better to clear it to force new setup next time.
    user_secret = db.query(UserSecret).filter(UserSecret.user_id == current_user.id).first()
    if user_secret:
        db.delete(user_secret)
        
    db.commit()
    return None
