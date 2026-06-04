from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from app.database import engine, Base
from app.api.health import router as health_router
from app.api.auth import router as auth_router

# Initialize FastAPI app
app = FastAPI(title="Your title", version="1.0")

# Allow CORS (Required for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security (use frontend URL in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(
    health_router,
    tags=["Health"]
)

app.include_router(auth_router)

# Create database tables(if using)
#Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to my first api"}
