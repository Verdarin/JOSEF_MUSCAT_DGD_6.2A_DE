from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from project.database import fs_sprite, db
from bson import ObjectId

# Create a router
router = APIRouter()

#Upload a sprite file
@router.post("/upload_sprite")
async def create_sprite(file: UploadFile = File(...)):
    try: # Try to create the sprite file
        file_id = await fs_sprite.upload_from_stream(file.filename, file.file) # Upload the file to GridFS
        return {"message": "Sprite created", "id": str(file_id)} # Return the file ID
    except Exception as e: # If the file is not found
        raise HTTPException(status_code=500, detail=str(e)) # Return a 500 error

#get all sprite files (metadata only)
@router.get("/get_sprite")
async def get_all_sprites():
    cursor = db["sprite.files"].find()  # GridFS files are stored in 'sprite.files'
    files = await cursor.to_list(length=None) # Convert the cursor to a list
    return [{"id": str(doc["_id"]), "filename": doc.get("filename", "")} for doc in files] # Return only the ID and filename

#get a sprite file by ID
@router.get("/get_sprite/{sprite_id}")
async def get_sprite(sprite_id: str):
    try: # Try to retrieve the sprite file
        stream = await fs_sprite.open_download_stream(ObjectId(sprite_id))
        content = await stream.read() # Read the file content
        
        #application/octet-stream is a generic binary file type
        return Response(content, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={stream.filename}"}) # Return the file content
    except Exception: # If the file is not found
        raise HTTPException(status_code=404, detail="Sprite not found") # Return a 404 error

#Update a sprite file by deleting the old one and uploading a new file
@router.put("/update_sprite/{sprite_id}")
async def update_sprite(sprite_id: str, file: UploadFile = File(...)):
    try: # Try to update the sprite file
        await fs_sprite.delete(ObjectId(sprite_id)) # Delete the existing file
        new_file_id = await fs_sprite.upload_from_stream(file.filename, file.file) # Upload the new file
        return {"message": "Sprite updated", "id": str(new_file_id)} # Return the new file ID
    except Exception as e: # If the file is not found
        raise HTTPException(status_code=404, detail="Sprite not found or update failed") # Return a 404 error

#Delete a sprite file
@router.delete("/delete_sprite/{sprite_id}")
async def delete_sprite(sprite_id: str):
    try: # Try to delete the sprite file
        await fs_sprite.delete(ObjectId(sprite_id)) # Delete the sprite file
        return {"message": "Sprite deleted"} # Return a success message
    except Exception: # If the file is not found
        raise HTTPException(status_code=404, detail="Sprite not found") # Return a 404 error
