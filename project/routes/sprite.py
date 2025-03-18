from fastapi import APIRouter, File, UploadFile
from project.database import db

# Create a router
router = APIRouter()

# Define a route for uploading sprite files
@router.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):
    content = await file.read() # Read the file content
    sprite_doc = {"filename": file.filename, "content": content} # Create a document
    result = await db.sprites.insert_one(sprite_doc) # Insert the document
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)} # Return the result
