from fastapi import APIRouter
from project.models import PlayerScore
from project.database import db

router = APIRouter()

@router.post("/player_score")
async def add_score(score: PlayerScore):
    score_doc = score.dict()
    result = await db.scores.insert_one(score_doc)
    return {"message": "Score recorded", "id": str(result.inserted_id)}
