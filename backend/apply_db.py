import os
import glob
from sqlalchemy import create_engine, text
from app.core.config import settings

def apply_sql_files():
    print(f"Connecting to {settings.SQLALCHEMY_DATABASE_URI}")
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    # Get all SQL files sorted
    sql_files = sorted(glob.glob("sql/*.sql"))
    
    with engine.connect() as connection:
        for file_path in sql_files:
            print(f"Applying {file_path}...")
            with open(file_path, "r") as f:
                sql_content = f.read()
                # Split by semicolon to handle multiple statements if needed, 
                # but SQLAlchemy execute(text()) might handle blocks.
                # Ideally, simple execution:
                try:
                    connection.execute(text(sql_content))
                    connection.commit()
                    print(f"  -> Success")
                except Exception as e:
                    print(f"  -> Failed: {e}")
                    connection.rollback()
                    # Don't exit, might be idempotent errors or partial setup
                    
if __name__ == "__main__":
    apply_sql_files()
