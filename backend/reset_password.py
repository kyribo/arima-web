from app.core.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext
from sqlalchemy import text

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def reset_admin_password():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "admin@arima.com").first()
        if not user:
            print("User admin@arima.com not found!")
            return

        new_hash = pwd_context.hash("Admin123!")
        print(f"Generated Hash: {new_hash}")
        
        # Direct SQL update to be 100% sure bypassing any model issues
        # But ORM is fine too.
        user.hashed_password = new_hash
        db.commit()
        db.refresh(user)
        print(f"Password updated successfully for {user.email}")
        print(f"Stored Hash in DB: {user.hashed_password}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin_password()
