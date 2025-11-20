from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from app.models.integrations import IntegrationsService, IntegrationProtocol
from app.api.storage import notification_service

router = APIRouter(prefix="/integrations", tags=["integrations"])

# Create a service instance
integrations_service = IntegrationsService()


class IntegrationCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    features: Optional[List[str]] = None
    commands: Optional[List[str]] = None


class IntegrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    status: str
    description: str
    features: List[str]
    commands: List[str]
    skills: List[str]
    connected: bool


class IntegrationStatsResponse(BaseModel):
    connected_count: int
    total_count: int


def _to_response(integration: IntegrationProtocol) -> IntegrationResponse:
    """Convert an Integration to IntegrationResponse."""
    return IntegrationResponse.model_validate(integration)


@router.post("/", response_model=IntegrationResponse)
def create_integration(request: IntegrationCreate):
    """Create a new integration."""
    integration = integrations_service.add_integration(
        name=request.name,
        description=request.description,
        features=request.features,
        commands=request.commands
    )
    
    # Send notification
    notification_service.send_notification(
        f"Integration '{integration.name}' has been created",
        integration.name,
        "integration_created"
    )
    
    return _to_response(integration)


@router.get("/", response_model=List[IntegrationResponse])
def get_integrations():
    """Get all integrations."""
    integrations = integrations_service.get_integrations()
    return [_to_response(i) for i in integrations]


@router.get("/stats", response_model=IntegrationStatsResponse)
def get_integration_stats():
    """Get integration statistics."""
    total_count = len(integrations_service.get_integrations())
    connected_count = integrations_service.get_connected_count()
    return IntegrationStatsResponse(
        connected_count=connected_count,
        total_count=total_count
    )


@router.get("/{name}", response_model=IntegrationResponse)
def get_integration(name: str):
    """Get a specific integration by name."""
    integration = integrations_service.get_integration(name)
    if not integration:
        raise HTTPException(status_code=404, detail=f"Integration '{name}' not found")
    return _to_response(integration)


@router.post("/{name}/activate", response_model=IntegrationResponse)
def activate_integration(name: str):
    """Activate an integration."""
    success = integrations_service.activate_integration(name)
    if not success:
        raise HTTPException(status_code=404, detail=f"Integration '{name}' not found")
    integration = integrations_service.get_integration(name)
    
    # Send notification
    notification_service.send_notification(
        f"Integration '{integration.name}' has been activated",
        integration.name,
        "integration_activated"
    )
    
    return _to_response(integration)


@router.post("/{name}/deactivate", response_model=IntegrationResponse)
def deactivate_integration(name: str):
    """Deactivate an integration."""
    success = integrations_service.deactivate_integration(name)
    if not success:
        raise HTTPException(status_code=404, detail=f"Integration '{name}' not found")
    integration = integrations_service.get_integration(name)
    
    # Send notification
    notification_service.send_notification(
        f"Integration '{integration.name}' has been deactivated",
        integration.name,
        "integration_deactivated"
    )
    
    return _to_response(integration)


@router.post("/{name}/toggle", response_model=IntegrationResponse)
def toggle_integration(name: str):
    """Toggle connection status of an integration."""
    success = integrations_service.toggle_connection(name)
    if not success:
        raise HTTPException(status_code=404, detail=f"Integration '{name}' not found")
    integration = integrations_service.get_integration(name)
    
    # Send notification
    connection_status = "connected" if integration.connected else "disconnected"
    notification_service.send_notification(
        f"Integration '{integration.name}' has been {connection_status}",
        integration.name,
        "integration_toggled"
    )
    
    return _to_response(integration)


@router.get("/{name}/skills", response_model=List[str])
def get_integration_skills(name: str):
    """Get skills for an integration (primarily for Alexa)."""
    integration = integrations_service.get_integration(name)
    if not integration:
        raise HTTPException(status_code=404, detail=f"Integration '{name}' not found")
    return integration.skills


class SkillRequest(BaseModel):
    skill: str


@router.post("/{name}/skills")
def add_integration_skill(name: str, request: SkillRequest):
    """Add a skill to an integration."""
    integration = integrations_service.get_integration(name)
    if not integration:
        raise HTTPException(status_code=404, detail=f"Integration '{name}' not found")
    if request.skill not in integration.skills:
        integration.skills.append(request.skill)
        
        # Send notification
        notification_service.send_notification(
            f"Skill '{request.skill}' added to integration '{name}'",
            name,
            "skill_added"
        )
    
    return {"message": f"Skill '{request.skill}' added to {name}"}

