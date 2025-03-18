from fastapi import APIRouter, HTTPException
from project.models import PlayerScore
from project.database import db
from bson import ObjectId

# Create a router
router = APIRouter()

#Create a new score
@router.post("/create_player_score")
async def create_score(score: PlayerScore): # Receive a PlayerScore Pydantic model
    doc = score.dict() # Convert the Pydantic model to a dictionary
    result = await db.scores.insert_one(doc) # Insert the new score
    return {"message": "Score created", "id": str(result.inserted_id)} # Return the new score ID

#GET all scores
@router.get("/get_player_score")
async def get_all_scores():
    cursor = db.scores.find() # Retrieve all scores
    scores = await cursor.to_list(length=None) # Convert the cursor to a list
    return [
        {"id": str(doc["_id"]), "player_name": doc["player_name"], "score": doc["score"]}
        for doc in scores
    ] # Return only the ID, player_name, and score for each score

#GET a score by ID
@router.get("/get_player_score/{score_id}")
async def get_score(score_id: str):
    doc = await db.scores.find_one({"_id": ObjectId(score_id)}) # Retrieve the score
    if not doc: # If the score is not found
        raise HTTPException(status_code=404, detail="Score not found") # Return a 404 error
    return {"id": str(doc["_id"]), "player_name": doc["player_name"], "score": doc["score"]} # Return the score

#Update an existing score by  ID
@router.put("/update_player_score/{score_id}")
async def update_score(score_id: str, score: PlayerScore):
    update_result = await db.scores.update_one({"_id": ObjectId(score_id)}, {"$set": score.dict()}) # Update the score
    if update_result.matched_count == 0: # If the score is not found
        raise HTTPException(status_code=404, detail="Score not found") # Return a 404 error
    return {"message": "Score updated"} # Return a success message

#Delete a score
@router.delete("/delete_player_score/{score_id}")
async def delete_score(score_id: str):
    delete_result = await db.scores.delete_one({"_id": ObjectId(score_id)}) # Delete the score
    if delete_result.deleted_count == 0: # If the score is not found
        raise HTTPException(status_code=404, detail="Score not found") # Return a 404 error
    return {"message": "Score deleted"} # Return a success message
