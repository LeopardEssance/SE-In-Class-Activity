from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

from app.models.integrations import IntegrationsService

router = APIRouter(prefix="/integrations", tags=["integrations"])

# Create a service instance
integrations_service = IntegrationsService()


class IntegrationCreate(BaseModel):
    name: str


class IntegrationResponse(BaseModel):
    name: str
    status: str
    
    class Config:
        from_attributes = True


@router.post("/", response_model=IntegrationResponse)
def create_integration(request: IntegrationCreate):
    """Create a new integration."""
    integration = integrations_service.add_integration(name=request.name)
    return IntegrationResponse(name=integration.name, status=integration.status)


@router.get("/", response_model=List[IntegrationResponse])
def get_integrations():
    """Get all integrations."""
    integrations = integrations_service.get_integrations()
    return [IntegrationResponse(name=i.name, status=i.status) for i in integrations]


@router.get("/{name}", response_model=IntegrationResponse)
def get_integration(name: str):
    """Get a specific integration by name."""
    integration = integrations_service.get_integration(name)
    if not integration:
        raise HTTPException(status_code=404, detail=f"Integration '{name}' not found")
    return IntegrationResponse(name=integration.name, status=integration.status)


@router.post("/{name}/activate", response_model=IntegrationResponse)
def activate_integration(name: str):
    """Activate an integration."""
    success = integrations_service.activate_integration(name)
    if not success:
        raise HTTPException(status_code=404, detail=f"Integration '{name}' not found")
    integration = integrations_service.get_integration(name)
    return IntegrationResponse(name=integration.name, status=integration.status)


@router.post("/{name}/deactivate", response_model=IntegrationResponse)
def deactivate_integration(name: str):
    """Deactivate an integration."""
    success = integrations_service.deactivate_integration(name)
    if not success:
        raise HTTPException(status_code=404, detail=f"Integration '{name}' not found")
    integration = integrations_service.get_integration(name)
    return IntegrationResponse(name=integration.name, status=integration.status)

