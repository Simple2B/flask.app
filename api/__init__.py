from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from config import config

from .utils import custom_generate_unique_id
from .routes import router

CFG = config()

app = FastAPI(version=CFG.VERSION, generate_unique_id_function=custom_generate_unique_id)
app.include_router(router)


@app.get("/", tags=["root"])
async def root():
    return RedirectResponse(url="/docs")
