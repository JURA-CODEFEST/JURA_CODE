from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def usingcors(app:FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://jura-frontend.vercel.app",
            # "http://127.0.0.1:5500"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )