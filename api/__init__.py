from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from config import config
from .routes import router

CFG = config()

app = FastAPI(version=CFG.VERSION)
app.include_router(router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
