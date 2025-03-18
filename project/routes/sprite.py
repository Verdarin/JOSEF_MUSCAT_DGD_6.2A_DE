from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from project.database import fs_sprite, db
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

#Upload a sprite file
@router.post("/upload_sprite")
async def create_sprite(file: UploadFile = File(...)):
    try: # Try to create the sprite file
        safe_filename = fix_filename(file.filename)  # Fix the filename before use
        file_id = await fs_sprite.upload_from_stream(safe_filename.filename, file.file) # Upload the file to GridFS
        return {"message": "Sprite created", "id": str(file_id)} # Return the file ID
    except Exception as e: # If the file is not found
        raise HTTPException(status_code=500, detail=str(e)) # Return a 500 error

#get all sprite files (metadata only)
@router.get("/get_sprite")
async def get_all_sprites():
    try: # Try to retrieve all sprite files
        cursor = db["sprite.files"].find()  # GridFS files are stored in 'sprite.files'
        files = await cursor.to_list(length=None) # Convert the cursor to a list
        return [{"id": str(doc["_id"]), "filename": doc.get("filename", "")} for doc in files] # Return only the ID and filename
    except Exception as e: # If the file is not found
        raise HTTPException(status_code=500, detail=str(e)) # Return a 500 error

#get a sprite file by ID
@router.get("/get_sprite/{sprite_id}")
async def get_sprite(sprite_id: str):
    try: # Try to retrieve the sprite file
        try: # Validate the sprite_id format
            obj_id = ObjectId(sprite_id) # Validate the sprite_id format
        except InvalidId: # If the sprite_id is invalid
            raise HTTPException(status_code=400, detail="Invalid sprite_id format") # If the sprite_id is invalid
        
        stream = await fs_sprite.open_download_stream(ObjectId(obj_id)) # Open a download stream
        content = await stream.read() # Read the file content
        #application/octet-stream is a generic binary file type that is used to send files that are not text files
        return Response(content, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={stream.filename}"}) # Return the file content
    except Exception: # If the file is not found
        raise HTTPException(status_code=404, detail="Sprite not found") # Return a 404 error

#Update a sprite file by deleting the old one and uploading a new file
@router.put("/update_sprite/{sprite_id}")
async def update_sprite(sprite_id: str, file: UploadFile = File(...)):
    try: # Try to update the sprite file
        try:
            obj_id = ObjectId(sprite_id) # Validate the sprite_id format
        except InvalidId: # If the sprite_id is invalid
            raise HTTPException(status_code=400, detail="Invalid sprite_id format") # Return a 400 error
        
        await fs_sprite.delete(ObjectId(obj_id)) # Delete the existing file
        safe_filename = fix_filename(file.filename)  # Fix the filename before use
        new_file_id = await fs_sprite.upload_from_stream(safe_filename.filename, file.file) # Upload the new file
        return {"message": "Sprite updated", "id": str(new_file_id)} # Return the new file ID
    except Exception as e: # If the file is not found
        raise HTTPException(status_code=404, detail="Sprite not found or update failed") # Return a 404 error

#Delete a sprite file
@router.delete("/delete_sprite/{sprite_id}")
async def delete_sprite(sprite_id: str):
    try: # Try to delete the sprite file
        try: # Validate the sprite_id format
            obj_id = ObjectId(sprite_id) # Validate the sprite_id format
        except InvalidId: # If the sprite_id is invalid
            raise HTTPException(status_code=400, detail="Invalid sprite_id format") # Return a 400 error
        
        await fs_sprite.delete(ObjectId(obj_id)) # Delete the sprite file
        return {"message": "Sprite deleted"} # Return a success message
    except Exception: # If the file is not found
        raise HTTPException(status_code=404, detail="Sprite not found") # Return a 404 error
