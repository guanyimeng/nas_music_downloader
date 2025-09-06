
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn


def create_app():
    version = "0.1.0"
    app = FastAPI(title="Nas Music Downloader Backend", version=version, description="Backend API for downloading music for Nas storage")

    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # You can restrict this to your frontend's origin
        allow_credentials=True,
        allow_methods=["*"],  # Or ["POST"] for more restriction
        allow_headers=["*"],
    )

    return app
    
if __name__ == "__main__":
    config = uvicorn.Config(
        create_app,
        host="0.0.0.0",
        port=8000
    )
    server = uvicorn.Server(config)
    server.run()