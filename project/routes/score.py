from fastapi import APIRouter
from project.models import PlayerScore
from project.database import db

# Create a router
router = APIRouter()

# Define a route for adding player scores
@router.post("/player_score")
async def add_score(score: PlayerScore):
    score_doc = score.dict() # Convert the Pydantic model to a dictionary
    result = await db.scores.insert_one(score_doc) # Insert the document
    return {"message": "Score recorded", "id": str(result.inserted_id)} # Return the result
