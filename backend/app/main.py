import app.models


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from app.database import engine, Base

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.test_rbac import (
    router as rbac_router
)
from app.api.api_keys import (
    router as api_key_router
)
from app.api.test_api_key import (
    router as test_api_key_router
)

from app.api.events import (
    router as event_router
)

from app.api.analytics import (
    router as analytics_router
)

from app.api.dashboards import (
    router as dashboard_router,
)

from app.api.widgets import (
    router as widget_router,
)

# Initialize FastAPI app
app = FastAPI(title="Your title", version="1.0")

# Allow CORS (Required for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],  # Adjust for security (use frontend URL in production)
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
app.include_router(rbac_router)
app.include_router(api_key_router)
app.include_router(test_api_key_router)
app.include_router(event_router)
app.include_router(analytics_router)
app.include_router(dashboard_router)
app.include_router(widget_router)
# Create database tables(if using)
#Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to my first api"}
