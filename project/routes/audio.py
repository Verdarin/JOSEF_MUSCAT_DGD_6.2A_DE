from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from project.database import fs_audio, db
from bson import ObjectId

# Create a router
router = APIRouter()

#Upload an audio file
@router.post("/upload_audio")
async def create_audio(file: UploadFile = File(...)):
    try: # Try to create the audio file
        file_id = await fs_audio.upload_from_stream(file.filename, file.file) # Upload the file to GridFS
        return {"message": "Audio created", "id": str(file_id)} # Return the file ID
    except Exception as e: # If the file is not found
        raise HTTPException(status_code=500, detail=str(e)) # Return a 500 error

#GET all audio files
@router.get("/get_audio")
async def get_all_audio():
    cursor = db["audio.files"].find()  # GridFS files are stored in 'audio.files'
    files = await cursor.to_list(length=None) # Convert the cursor to a list
    return [{"id": str(doc["_id"]), "filename": doc.get("filename", "")} for doc in files] # Return only the ID and filename

#Retrieve an audio file by ID
@router.get("/get_audio/{audio_id}")
async def get_audio(audio_id: str):
    try: # Try to retrieve the audio file
        stream = await fs_audio.open_download_stream(ObjectId(audio_id)) # Open a download stream
        content = await stream.read() # Read the file content
        
        #application/octet-stream is a generic binary file type
        return Response(content, media_type="application/octet-stream", 
                        headers={"Content-Disposition": f"attachment; filename={stream.filename}"}) # Return the file content
    except Exception: # If the file is not found
        raise HTTPException(status_code=404, detail="Audio not found") # Return a 404 error

#Update an audio file by deleting the old one and uploading a new file
@router.put("/update_audio/{audio_id}")
async def update_audio(audio_id: str, file: UploadFile = File(...)):
    try: # Try to update the audio file
        await fs_audio.delete(ObjectId(audio_id)) # Delete the existing file
        new_file_id = await fs_audio.upload_from_stream(file.filename, file.file) # Upload the new file
        return {"message": "Audio updated", "id": str(new_file_id)} # Return the new file ID
    except Exception as e: # If the file is not found
        raise HTTPException(status_code=404, detail="Audio not found or update failed") # Return a 404 error

#Delete an audio file
@router.delete("/delete_audio/{audio_id}")
async def delete_audio(audio_id: str):
    try: # Try to delete the audio file
        await fs_audio.delete(ObjectId(audio_id)) # Delete the audio file
        return {"message": "Audio deleted"} # Return a success message
    except Exception: # If the file is not found
        raise HTTPException(status_code=404, detail="Audio not found") # Return a 404 error
