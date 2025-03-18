from fastapi import FastAPI
from project.routes.audio import router as audio_router
from project.routes.sprite import router as sprite_router
from project.routes.score import router as score_router

app = FastAPI()

app.include_router(audio_router)
app.include_router(sprite_router)
app.include_router(score_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("project.main:app", host="127.0.0.1", port=8000, reload=True)
