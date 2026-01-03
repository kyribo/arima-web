from sqlalchemy import create_engine, text
import os

# Using localhost for script execution
DATABASE_URL = "postgresql://arimadev:rizkytampan@localhost:5432/arimadev"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("Adding access column...")
        connection.execute(text("ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS access JSONB DEFAULT '[]'::jsonb;"))
        connection.commit()
        print("Column added successfully.")
except Exception as e:
    print(f"Error: {e}")
