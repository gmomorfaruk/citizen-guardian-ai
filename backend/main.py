from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, auth, items, documents, ai # <-- IMPORT ai

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Citizen Guardian AI API",
    description="API for managing citizen information and AI-powered services.",
    version="0.1.0",
)

# Include the routers
app.include_router(users.router, prefix="/api/v1", tags=["Users & Registration"])
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(items.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1") # <-- ADD THIS LINE

@app.get("/")
def read_root():
    return {"message": "Welcome to the Citizen Guardian AI API"}