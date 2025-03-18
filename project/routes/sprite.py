from fastapi import APIRouter, File, UploadFile
from project.database import db

router = APIRouter()

@router.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):
    content = await file.read()
    sprite_doc = {"filename": file.filename, "content": content}
    result = await db.sprites.insert_one(sprite_doc)
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}
