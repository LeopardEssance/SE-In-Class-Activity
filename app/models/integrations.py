from typing import List, Optional


class Integration:
    """Represents an external integration."""
    def __init__(self, name: str, status: str = "inactive"):
        self.name = name
        self.status = status  # active, inactive, error


class IntegrationsService:
    """Service class for managing integrations."""
    
    def __init__(self):
        self.integrations: List[Integration] = []
    
    def add_integration(self, name: str) -> Integration:
        """Add a new integration."""
        integration = Integration(name=name, status="inactive")
        self.integrations.append(integration)
        return integration
    
    def get_integrations(self) -> List[Integration]:
        """Get all integrations."""
        return self.integrations
    
    def get_integration(self, name: str) -> Optional[Integration]:
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

