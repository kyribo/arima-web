from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from dotenv import load_dotenv
import os

from database import engine, Base, get_db

load_dotenv()

# Tables should be created via migrations (Alembic), not automatically at startup.
# Base.metadata.create_all(bind=engine)

app = FastAPI(title=os.getenv("APP_NAME", "FastAPI App"))

# CORS Configuration
origins = [
    "http://localhost:5173", # SvelteKit default port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root(db: Session = Depends(get_db)):
    if db is None:
        db_status = "disconnected"
    else:
        try:
            db.execute(text("SELECT 1"))
            db_status = "connected"
        except Exception:
            db_status = "disconnected"

    return {
        "app": os.getenv("APP_NAME", "FastAPI App"),
        "status": "running",
        "database": db_status
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
