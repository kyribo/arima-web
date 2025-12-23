from app.core.database import SessionLocal
from app.models.user import User
from app.models.session import Session
from app.models.user_secret import UserSecret

def reset_2fa():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "admin@arima.com").first()
        if user:
            print(f"Found user {user.email}. is_2fa_enabled={user.is_2fa_enabled}")
            user.is_2fa_enabled = False
            
            # Use delete instead of filter().delete() for cascade if relationship set, 
            # but here explicit is fine.
            db.query(UserSecret).filter(UserSecret.user_id == user.id).delete()
            
            db.commit()
            print("2FA disabled and secret removed.")
        else:
            print("User not found.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_2fa()
