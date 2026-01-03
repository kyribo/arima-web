from app.core.database import SessionLocal
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    db = SessionLocal()
    try:
        with open("sql/03-01-risk-init.sql", "r") as f:
            sql_script = f.read()
        
        # Split by statements if needed, but text() can handle blocks often. 
        # Safer to execute the whole block if using psql mechanism, but via sqlalchemy:
        # We'll try executing as one block. If it fails due to multiple statements, we split.
        
        logger.info("Executing Migration: 03-add-risk-tables.sql")
        db.execute(text(sql_script))
        db.commit()
        logger.info("Migration successful!")
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
