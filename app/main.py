from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .init_db import init_db

app = FastAPI(
    title="JSONPlaceholder API",
    description="A full-featured RESTful API that replicates JSONPlaceholder with authentication",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to JSONPlaceholder API"}

# Import and include routers
from app.routers import users, auth

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"]) 