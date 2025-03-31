from fastapi import APIRouter, File, UploadFile, HTTPException, Response, Depends
from project.database import get_fs_audio, get_db
from bson import ObjectId
from bson.errors import InvalidId
import re

# Create a router
router = APIRouter()

def fix_filename(filename: str) -> str:
    # Allow only letters, numbers, underscore, dash, and dot; replace others with underscore.
    # This is to prevent directory traversal attacks.
    # For example, if the filename is "../../etc/passwd", it could be saved in a different directory.
    # The fixed filename would be "______etc_passwd".
    return re.sub(r'[^A-Za-z0-9._-]', '_', filename) # Allow only letters, numbers, underscore, dash, and dot; replace others with underscore.

#Upload an audio file
@router.post("/upload_audio")
async def create_audio(file: UploadFile = File(...), fs_audio = Depends(get_fs_audio)):
    try: # Try to create the audio file
        safe_filename = fix_filename(file.filename)  # Fix the filename before use
        file_id = await fs_audio.upload_from_stream(safe_filename, file.file) # Upload the file to GridFS
        return {"message": "Audio created", "id": str(file_id)} # Return the file ID
    except Exception as e: # If the file is not found
        raise HTTPException(status_code=500, detail=str(e)) # Return a 500 error

#GET all audio files
@router.get("/get_audio")
async def get_all_audio(db = Depends(get_db)):
    cursor = db["audio.files"].find()  # GridFS files are stored in 'audio.files'
    files = await cursor.to_list(length=None) # Convert the cursor to a list
    return [{"id": str(doc["_id"]), "filename": doc.get("filename", "")} for doc in files] # Return only the ID and filename

#Retrieve an audio file by ID
@router.get("/get_audio/{audio_id}")
async def get_audio(audio_id: str, fs_audio = Depends(get_fs_audio)):
    try: # Try to retrieve the audio file
        try: # Validate the audio_id format
            obj_id = ObjectId(audio_id) # Validate the audio_id format
        except InvalidId: # If the audio_id is invalid
            raise HTTPException(status_code=400, detail="Invalid audio_id format") # If the audio_id is invalid
        
        stream = await fs_audio.open_download_stream(ObjectId(obj_id)) # Open a download stream
        content = await stream.read() # Read the file content
            
        #application/octet-stream is a generic binary file type
        return Response(content, media_type="application/octet-stream",  headers={"Content-Disposition": f"attachment; filename={stream.filename}"}) # Return the file content
    except Exception: # If the file is not found
        raise HTTPException(status_code=404, detail="Audio not found") # Return a 404 error

#Update an audio file by deleting the old one and uploading a new file
@router.put("/update_audio/{audio_id}")
async def update_audio(audio_id: str, file: UploadFile = File(...),fs_audio = Depends(get_fs_audio)):
    try: # Try to update the audio file
        try: # Validate the audio_id format
            obj_id = ObjectId(audio_id) # Validate the audio_id format
        except InvalidId: # If the audio_id is invalid
            raise HTTPException(status_code=400, detail="Invalid audio_id format") # Return a 400 error
        
        await fs_audio.delete(ObjectId(obj_id)) # Delete the existing file
        safe_filename = fix_filename(file.filename)  # Fix the filename before use
        new_file_id = await fs_audio.upload_from_stream(safe_filename, file.file) # Upload the new file
        return {"message": "Audio updated", "id": str(new_file_id)} # Return the new file ID
    except Exception as e: # If the file is not found
        raise HTTPException(status_code=404, detail="Audio not found or update failed") # Return a 404 error

#Delete an audio file
@router.delete("/delete_audio/{audio_id}")
async def delete_audio(audio_id: str, fs_audio = Depends(get_fs_audio)):
    try: # Try to delete the audio file
        try: # Validate the audio_id format
            obj_id = ObjectId(audio_id) # Validate the audio_id format
        except InvalidId: # If the audio_id is invalid
            raise HTTPException(status_code=400, detail="Invalid audio_id format") # Return a 400 error
        
        await fs_audio.delete(ObjectId(obj_id)) # Delete the audio file
        return {"message": "Audio deleted"} # Return a success message
    except Exception: # If the file is not found
        raise HTTPException(status_code=404, detail="Audio not found") # Return a 404 error
