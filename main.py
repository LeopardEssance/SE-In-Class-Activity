from fastapi import FastAPI
from app.api import integrations

app = FastAPI(title="SE In-Class Activity API", version="1.0.0")

# Include routers
app.include_router(integrations.router)

@app.get("/")
def root():
    return {"message": "SE In-Class Activity API"}

