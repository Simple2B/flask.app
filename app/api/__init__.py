from fastapi import FastAPI, APIRouter

app = FastAPI(root_path="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}
