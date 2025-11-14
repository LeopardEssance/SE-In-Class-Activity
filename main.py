from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import integrations, auth, devices, scheduler

app = FastAPI(
    title="SE In-Class Activity API",
    description="Backend API for Smart Home IoT System with device control and scheduling",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(integrations.router)
app.include_router(auth.router)
app.include_router(devices.router)
app.include_router(scheduler.router)


@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "message": "SE In-Class Activity API",
        "version": "1.0.0"
    }
