"""
Integration tests for the Integrations API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root(self):
        """Test root endpoint returns correct message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "SE In-Class Activity API"}


class TestGetIntegrations:
    """Tests for GET /integrations/ endpoint."""
    
    def test_get_all_integrations(self):
        """Test getting all integrations."""
        response = client.get("/integrations/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3  # Should have at least 3 default integrations
        
        # Check that default integrations exist
        names = [integration["name"] for integration in data]
        assert "Amazon Alexa" in names
        assert "Google Assistant" in names
        assert "Apple Homekit" in names
    
    def test_integration_structure(self):
        """Test that integration objects have correct structure."""
        response = client.get("/integrations/")
        assert response.status_code == 200
        data = response.json()
        
        if data:
            integration = data[0]
            assert "name" in integration
            assert "status" in integration
            assert "description" in integration
            assert "features" in integration
            assert "commands" in integration
            assert "skills" in integration
            assert "connected" in integration


class TestGetIntegrationStats:
    """Tests for GET /integrations/stats endpoint."""
    
    def test_get_stats(self):
        """Test getting integration statistics."""
        response = client.get("/integrations/stats")
        assert response.status_code == 200
        data = response.json()
        assert "connected_count" in data
        assert "total_count" in data
        assert isinstance(data["connected_count"], int)
        assert isinstance(data["total_count"], int)
        assert data["total_count"] >= 3
        assert data["connected_count"] >= 0


class TestGetIntegrationByName:
    """Tests for GET /integrations/{name} endpoint."""
    
    def test_get_alexa_integration(self):
        """Test getting Amazon Alexa integration."""
        response = client.get("/integrations/Amazon Alexa")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Amazon Alexa"
        assert "description" in data
        assert "features" in data
        assert "commands" in data
        assert len(data["commands"]) > 0  # Alexa should have commands
    
    def test_get_google_assistant_integration(self):
        """Test getting Google Assistant integration."""
        response = client.get("/integrations/Google Assistant")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Google Assistant"
        assert "description" in data
    
    def test_get_homekit_integration(self):
        """Test getting Apple Homekit integration."""
        response = client.get("/integrations/Apple Homekit")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Apple Homekit"
        assert "description" in data
    
    def test_get_nonexistent_integration(self):
        """Test getting non-existent integration returns 404."""
        response = client.get("/integrations/NonExistentIntegration")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestCreateIntegration:
    """Tests for POST /integrations/ endpoint."""
    
    def test_create_integration_minimal(self):
        """Test creating integration with minimal data."""
        response = client.post(
            "/integrations/",
            json={"name": "Test Integration Minimal"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Integration Minimal"
        assert data["status"] == "inactive"
        assert data["connected"] is False
    
    def test_create_integration_full(self):
        """Test creating integration with all fields."""
        response = client.post(
            "/integrations/",
            json={
                "name": "Test Integration Full",
                "description": "Test description",
                "features": ["Feature 1", "Feature 2"],
                "commands": ["Command 1", "Command 2"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Integration Full"
        assert data["description"] == "Test description"
        assert data["features"] == ["Feature 1", "Feature 2"]
        assert data["commands"] == ["Command 1", "Command 2"]
    
    def test_create_integration_optional_fields(self):
        """Test creating integration with optional fields."""
        response = client.post(
            "/integrations/",
            json={
                "name": "Test Integration Optional",
                "description": "Optional description"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Integration Optional"
        assert data["description"] == "Optional description"
        assert data["features"] == []
        assert data["commands"] == []


class TestActivateIntegration:
    """Tests for POST /integrations/{name}/activate endpoint."""
    
    def test_activate_integration(self):
        """Test activating an integration."""
        # First create an inactive integration
        client.post(
            "/integrations/",
            json={"name": "Test Activate Integration"}
        )
        
        # Activate it
        response = client.post("/integrations/Test Activate Integration/activate")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Activate Integration"
        assert data["status"] == "active"
    
    def test_activate_alexa(self):
        """Test activating Amazon Alexa (already active)."""
        response = client.post("/integrations/Amazon Alexa/activate")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Amazon Alexa"
        assert data["status"] == "active"
    
    def test_activate_nonexistent_integration(self):
        """Test activating non-existent integration returns 404."""
        response = client.post("/integrations/NonExistent/activate")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestDeactivateIntegration:
    """Tests for POST /integrations/{name}/deactivate endpoint."""
    
    def test_deactivate_integration(self):
        """Test deactivating an integration."""
        # First create and activate an integration
        client.post(
            "/integrations/",
            json={"name": "Test Deactivate Integration"}
        )
        client.post("/integrations/Test Deactivate Integration/activate")
        
        # Deactivate it
        response = client.post("/integrations/Test Deactivate Integration/deactivate")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Deactivate Integration"
        assert data["status"] == "inactive"
    
    def test_deactivate_nonexistent_integration(self):
        """Test deactivating non-existent integration returns 404."""
        response = client.post("/integrations/NonExistent/deactivate")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestToggleIntegration:
    """Tests for POST /integrations/{name}/toggle endpoint."""
    
    def test_toggle_integration_from_false_to_true(self):
        """Test toggling integration connection from false to true."""
        # Create an integration with connected=False
        client.post(
            "/integrations/",
            json={"name": "Test Toggle Integration"}
        )
        
        # Toggle it
        response = client.post("/integrations/Test Toggle Integration/toggle")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Toggle Integration"
        assert data["connected"] is True
    
    def test_toggle_integration_from_true_to_false(self):
        """Test toggling integration connection from true to false."""
        # Create an integration and toggle it to True
        client.post(
            "/integrations/",
            json={"name": "Test Toggle Integration 2"}
        )
        client.post("/integrations/Test Toggle Integration 2/toggle")
        
        # Toggle it again to False
        response = client.post("/integrations/Test Toggle Integration 2/toggle")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Toggle Integration 2"
        assert data["connected"] is False
    
    def test_toggle_nonexistent_integration(self):
        """Test toggling non-existent integration returns 404."""
        response = client.post("/integrations/NonExistent/toggle")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestGetIntegrationSkills:
    """Tests for GET /integrations/{name}/skills endpoint."""
    
    def test_get_alexa_skills(self):
        """Test getting skills for Amazon Alexa."""
        response = client.get("/integrations/Amazon Alexa/skills")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_skills_empty(self):
        """Test getting skills for integration with no skills."""
        # Create a new integration
        client.post(
            "/integrations/",
            json={"name": "Test Skills Integration"}
        )
        
        response = client.get("/integrations/Test Skills Integration/skills")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_skills_nonexistent_integration(self):
        """Test getting skills for non-existent integration returns 404."""
        response = client.get("/integrations/NonExistent/skills")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestAddIntegrationSkill:
    """Tests for POST /integrations/{name}/skills endpoint."""
    
    def test_add_skill_to_integration(self):
        """Test adding a skill to an integration."""
        # Create a new integration
        client.post(
            "/integrations/",
            json={"name": "Test Add Skill Integration"}
        )
        
        # Add a skill
        response = client.post(
            "/integrations/Test Add Skill Integration/skills",
            json={"skill": "Test Skill 1"}
        )
        assert response.status_code == 200
        assert "added" in response.json()["message"].lower()
        
        # Verify skill was added
        skills_response = client.get("/integrations/Test Add Skill Integration/skills")
        assert skills_response.status_code == 200
        skills = skills_response.json()
        assert "Test Skill 1" in skills
    
    def test_add_multiple_skills(self):
        """Test adding multiple skills to an integration."""
        # Create a new integration
        client.post(
            "/integrations/",
            json={"name": "Test Multiple Skills Integration"}
        )
        
        # Add first skill
        client.post(
            "/integrations/Test Multiple Skills Integration/skills",
            json={"skill": "Skill 1"}
        )
        
        # Add second skill
        client.post(
            "/integrations/Test Multiple Skills Integration/skills",
            json={"skill": "Skill 2"}
        )
        
        # Verify both skills were added
        skills_response = client.get("/integrations/Test Multiple Skills Integration/skills")
        assert skills_response.status_code == 200
        skills = skills_response.json()
        assert "Skill 1" in skills
        assert "Skill 2" in skills
        assert len(skills) == 2
    
    def test_add_duplicate_skill(self):
        """Test adding duplicate skill doesn't create duplicates."""
        # Create a new integration
        client.post(
            "/integrations/",
            json={"name": "Test Duplicate Skill Integration"}
        )
        
        # Add skill twice
        client.post(
            "/integrations/Test Duplicate Skill Integration/skills",
            json={"skill": "Duplicate Skill"}
        )
        client.post(
            "/integrations/Test Duplicate Skill Integration/skills",
            json={"skill": "Duplicate Skill"}
        )
        
        # Verify skill appears only once
        skills_response = client.get("/integrations/Test Duplicate Skill Integration/skills")
        assert skills_response.status_code == 200
        skills = skills_response.json()
        assert skills.count("Duplicate Skill") == 1
    
    def test_add_skill_to_nonexistent_integration(self):
        """Test adding skill to non-existent integration returns 404."""
        response = client.post(
            "/integrations/NonExistent/skills",
            json={"skill": "Test Skill"}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestIntegrationWorkflow:
    """Tests for complete integration workflows."""
    
    def test_complete_integration_lifecycle(self):
        """Test complete lifecycle of an integration."""
        # Create integration
        create_response = client.post(
            "/integrations/",
            json={
                "name": "Lifecycle Test Integration",
                "description": "Test lifecycle",
                "features": ["Feature 1"]
            }
        )
        assert create_response.status_code == 200
        assert create_response.json()["status"] == "inactive"
        assert create_response.json()["connected"] is False
        
        # Activate integration
        activate_response = client.post("/integrations/Lifecycle Test Integration/activate")
        assert activate_response.status_code == 200
        assert activate_response.json()["status"] == "active"
        
        # Toggle connection
        toggle_response = client.post("/integrations/Lifecycle Test Integration/toggle")
        assert toggle_response.status_code == 200
        assert toggle_response.json()["connected"] is True
        
        # Add skills
        client.post(
            "/integrations/Lifecycle Test Integration/skills",
            json={"skill": "Lifecycle Skill 1"}
        )
        client.post(
            "/integrations/Lifecycle Test Integration/skills",
            json={"skill": "Lifecycle Skill 2"}
        )
        
        # Verify final state
        final_response = client.get("/integrations/Lifecycle Test Integration")
        assert final_response.status_code == 200
        final_data = final_response.json()
        assert final_data["status"] == "active"
        assert final_data["connected"] is True
        assert len(final_data["skills"]) == 2
        
        # Deactivate
        deactivate_response = client.post("/integrations/Lifecycle Test Integration/deactivate")
        assert deactivate_response.status_code == 200
        assert deactivate_response.json()["status"] == "inactive"
    
    def test_stats_update_with_workflow(self):
        """Test that stats update correctly during workflow."""
        # Get initial stats
        initial_stats = client.get("/integrations/stats").json()
        initial_connected = initial_stats["connected_count"]
        initial_total = initial_stats["total_count"]
        
        # Create and connect new integration
        client.post(
            "/integrations/",
            json={"name": "Stats Test Integration"}
        )
        client.post("/integrations/Stats Test Integration/toggle")
        
        # Get updated stats
        updated_stats = client.get("/integrations/stats").json()
        assert updated_stats["total_count"] == initial_total + 1
        assert updated_stats["connected_count"] == initial_connected + 1

