from fastapi import FastAPI
from project.routes.audio import router as audio_router
from project.routes.sprite import router as sprite_router
from project.routes.score import router as score_router

# Create the FastAPI instance
app = FastAPI()

# Include the routers
app.include_router(audio_router)
app.include_router(sprite_router)
app.include_router(score_router)

# Run the application with Uvicorn
if __name__ == "__main__":
    import uvicorn 
    # Run the application with Uvicorn
    uvicorn.run("project.main:app", host="127.0.0.1", port=8000, reload=True)
