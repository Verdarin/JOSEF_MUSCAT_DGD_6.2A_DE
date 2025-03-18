# app.py
from fastapi import FastAPI
from routes.sprite import router as sprite_router
from routes.audio import router as audio_router
from routes.score import router as score_router

app = FastAPI()

app.include_router(sprite_router)
app.include_router(audio_router)
app.include_router(score_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
