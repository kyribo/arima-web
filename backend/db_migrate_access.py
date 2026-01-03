import os
import psycopg2

# Connection details from .env (hardcoding based on known usage to ensure it works in this context)
host = "localhost"
database = "arimadev"
user = "arimadev"
password = "rizkytampan"

try:
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("Adding access column...")
    cursor.execute("ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS access JSONB DEFAULT '[]'::jsonb;")
    print("Column added successfully.")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
