from pydantic import BaseModel, Field

# Define the model for the PlayerScore
class PlayerScore(BaseModel):
    
    #... indicates that the field is required
    # Field() is used to define additional constraints for the field
    # min_length=1 and max_length=50 are used to define the minimum and maximum length of the player_name
    # regex=r'^[A-Za-z0-9\s]+$' is used to define a regular expression pattern for the player_name
    # ge=0 is used to define that the score must be greater than or equal to 0
    player_name: str = Field(..., min_length=1, max_length=50, regex=r'^[A-Za-z0-9\s]+$')
    score: int = Field(..., ge=0)