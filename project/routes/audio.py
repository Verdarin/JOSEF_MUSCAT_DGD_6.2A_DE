from fastapi import APIRouter, File, UploadFile, HTTPException
from project.database import fs
from bson import ObjectId

# Create a router
router = APIRouter()

#Upload audio file to GridFS
# Define a route for uploading audio files
@router.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # fs.upload_from_stream() will read the file and store it in GridFS
        file_id = await fs.upload_from_stream(
            file.filename,
            file.file  # file-like object from FastAPI's UploadFile
        )
        return {"message": "Audio uploaded", "file_id": str(file_id)} # Return the result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # Raise an exception if an error occurs