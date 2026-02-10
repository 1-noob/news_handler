# API entry point

from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Articlux API",
    version="1.0.0",
    description="API for Articlux, a knowledge graph management system."
)

app.include_router(router)