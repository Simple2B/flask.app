from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .routes import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
