from fastapi import FastAPI
from routes.upload import router as upload_router

app=FastAPI(
    title="LogLens API",
    description="Playback log analysis and investigation backend",
    version="1.0.0"
)
app.include_router(
    upload_router,
    prefix="/api/logs"
)
@app.get("/")
def root():
    return{
        "message":"LogLens backend is running"
    }