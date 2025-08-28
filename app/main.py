from fastapi import FastAPI

app = FastAPI(title="Moon Robot Control API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Moon Robot Control API"}