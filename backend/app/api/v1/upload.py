from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
import os
import uuid
from typing import Dict

router = APIRouter()

UPLOAD_DIR = "static/uploads"

@router.post("/", response_model=Dict[str, str])
async def upload_file(file: UploadFile = File(...)):
    try:
        # Validate file type (basic)
        if not file.content_type.startswith("image/"):
             raise HTTPException(status_code=400, detail="Only images are allowed")

        # Generate unique filename
        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return relative URL
        return {"url": f"/static/uploads/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
