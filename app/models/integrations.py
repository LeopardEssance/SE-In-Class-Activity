from typing import List, Optional, Protocol
from dataclasses import dataclass, field


class IntegrationProtocol(Protocol):
    """Protocol defining the interface for integration objects."""
    name: str
    status: str
    description: str
    features: List[str]
    commands: List[str]
    skills: List[str]
    connected: bool


@dataclass
class Integration:
    """Represents an external integration."""
    name: str
    status: str = "inactive"  # active, inactive, error
    description: str = ""
    features: List[str] = field(default_factory=list)
    commands: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    connected: bool = False


class IntegrationsService:
    """Service class for managing integrations."""
    
    def __init__(self):
        self.integrations: List[IntegrationProtocol] = []
        self.initialize_default_integrations()
    
    def add_integration(self, name: str, description: str = "", features: List[str] = None,
                       commands: List[str] = None, skills: List[str] = None, 
                       connected: bool = False) -> IntegrationProtocol:
        """Add a new integration."""
        integration = Integration(
            name=name, status="inactive", description=description,
            features=features or [], commands=commands or [], skills=skills or [], connected=connected
        )
        self.integrations.append(integration)
        return integration
    
    def get_integrations(self) -> List[IntegrationProtocol]:
        """Get all integrations."""
        return self.integrations
    
    def get_integration(self, name: str) -> Optional[IntegrationProtocol]:
        """Get a specific integration by name."""
        for integration in self.integrations:
            if integration.name == name:
                return integration
        return None
    
    def activate_integration(self, name: str) -> bool:
        """Activate an integration."""
        integration = self.get_integration(name)
        if integration:
            integration.status = "active"
            return True
        return False
    
    def deactivate_integration(self, name: str) -> bool:
        """Deactivate an integration."""
        integration = self.get_integration(name)
        if integration:
            integration.status = "inactive"
            return True
        return False
    
    def get_connected_count(self) -> int:
        """Get count of connected integrations."""
        return sum(1 for integration in self.integrations if integration.connected)
    
    def toggle_connection(self, name: str) -> bool:
        """Toggle connection status of an integration."""
        integration = self.get_integration(name)
        if integration:
            integration.connected = not integration.connected
            return True
        return False
    
    def initialize_default_integrations(self):
        """Initialize default integrations (Alexa, Google Assistant, Homekit)."""
        # Amazon Alexa
        self.add_integration(
            name="Amazon Alexa",
            description="control your smart home with voice commands",
            features=["Voice controls", "Smart home skills"],
            commands=[
                "Alexa turn on the living room lights",
                "Alexa Set the thermostats to 72 degrees",
                "Alexa show me the front door camera"
            ],
            skills=[],
            connected=True
        )
        self.activate_integration("Amazon Alexa")
        
        # Google Assistant
        self.add_integration(
            name="Google Assistant",
            description="Manage Devices with google voice commands",
            features=["Voice controls", "Smart home skills"],
            connected=False
        )
        
        # Apple Homekit
        self.add_integration(
            name="Apple Homekit",
            description="Integrate with Apple homekit ecosystem",
            features=["Voice controls", "Smart home skills"],
            connected=False
        )

