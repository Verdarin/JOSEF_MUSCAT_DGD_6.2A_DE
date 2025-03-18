from pydantic import BaseModel

# Create a Pydantic model for the PlayerScore
class PlayerScore(BaseModel):
    player_name: str
    score: int
