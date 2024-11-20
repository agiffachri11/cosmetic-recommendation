from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_route
from app.config.firebase_config import initialize_firebase

firebase_app = initialize_firebase()

app = FastAPI(
    title="Cosmetic Recommendation API Authentication",
    description="API Authentication with FastAPI and Firebase",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_route.router, prefix="/api", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Welcome to Cosmetic Recommendation API Authentication"}