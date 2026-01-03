from sqlalchemy import create_engine, text
from app.core.security import get_password_hash
from app.core.config import settings
import uuid

# Setup DB connection
DATABASE_URL = "postgresql://arimadev:rizkytampan@localhost:5432/arimadev"
engine = create_engine(DATABASE_URL)

def create_admin():
    username = "test_admin_auto"
    password = "password123"
    hashed = get_password_hash(password)
    
    with engine.connect() as conn:
        # Check if exists
        res = conn.execute(text("SELECT id FROM auth.users WHERE username = :u"), {"u": username})
        if res.fetchone():
            print("User exists")
            return

        conn.execute(text("""
            INSERT INTO auth.users (id, username, email, hashed_password, role, is_active, is_2fa_enabled, created_at, updated_at)
            VALUES (:id, :u, :e, :h, :r, :a, :tfa, now(), now())
        """), {
            "id": uuid.uuid4(),
            "u": username,
            "e": "test_admin@example.com",
            "h": hashed,
            "r": "Superadmin",
            "a": True,
            "tfa": False
        })
        conn.commit()
        print(f"Created admin: {username} / {password}")

if __name__ == "__main__":
    create_admin()
