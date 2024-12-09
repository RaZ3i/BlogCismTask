from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth.router import router as auth_router
from src.profile_oper.router import router as profile_oper_router
from src.pages.router import router as pages_router

app = FastAPI(title="Blog")
app.mount("/static", StaticFiles(directory="src/static", html=True), name="static")
app.include_router(auth_router)
app.include_router(profile_oper_router)
app.include_router(pages_router)
