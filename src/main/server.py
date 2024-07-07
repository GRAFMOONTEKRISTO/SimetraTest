from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers import routers

app = FastAPI()

origins = [
    "http://localhost:5473",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Set-Cookie", "Authorization", "Access-Control-Allow-Origin",
                   "Access-Control-Allow-Headers"]
)

app.include_router(routers)
