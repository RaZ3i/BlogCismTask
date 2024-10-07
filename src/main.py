from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.auth.router import router as auth_router
from src.profile_oper.router import router as profile_oper_router
from src.pages.router import router as pages_router

app = FastAPI(title="Blog")
app.mount("/static", StaticFiles(directory="src/static", html=True), name="static")
app.include_router(auth_router)
app.include_router(profile_oper_router)
app.include_router(pages_router)

# origins = [
#     "http://127.0.0.1:5500",
#     "http://localhost:5500",
#     "http://127.0.0.1:8087",
#     "http://localhost:8087",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "DELETE", "PATCH", "PUT", "OPTIONS"],
#     allow_headers=[
#         "Content-Type",
#         "Access-Control-Allow-Headers",
#         "Access-Control-Allow-Origin",
#         "Authorization",
#     ],
# )
