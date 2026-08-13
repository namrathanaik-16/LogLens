from fastapi import FastAPI
app=FastAPI(
    title="LogLens API",
    description="Playback log analysis and investigation backend",
    version="1.0.0"
)
@app.get("/")
def root():
    return{
        "message":"LogLens backend in running"
    }