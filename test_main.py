import pytest
import httpx
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAuth:
    def test_register_user(self):
        """Test user registration."""
        response = client.post("/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "id" in data

    def test_login_user(self):
        """Test user login."""
        # First register a user
        client.post("/auth/register", json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "loginpassword123"
        })
        
        # Then login
        response = client.post("/auth/login", json={
            "username": "loginuser",
            "password": "loginpassword123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

class TestNotes:
    def setup_method(self):
        """Setup method to create a user and get token."""
        # Register user
        client.post("/auth/register", json={
            "username": "noteuser",
            "email": "note@example.com",
            "password": "notepassword123"
        })
        
        # Login and get token
        response = client.post("/auth/login", json={
            "username": "noteuser",
            "password": "notepassword123"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_create_note(self):
        """Test note creation."""
        response = client.post("/notes", 
            json={"title": "Test Note", "content": "This is a test note"},
            headers=self.headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Note"
        assert data["content"] == "This is a test note"
        assert data["version"] == 1

    def test_get_notes(self):
        """Test getting user notes."""
        # Create a note first
        client.post("/notes", 
            json={"title": "Test Note", "content": "This is a test note"},
            headers=self.headers
        )
        
        response = client.get("/notes", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == "Test Note"

    def test_update_note_optimistic_locking(self):
        """Test note update with optimistic locking."""
        # Create a note
        create_response = client.post("/notes", 
            json={"title": "Original Title", "content": "Original content"},
            headers=self.headers
        )
        note_data = create_response.json()
        note_id = note_data["id"]
        
        # Update with correct version
        response = client.put(f"/notes/{note_id}", 
            json={
                "title": "Updated Title",
                "content": "Updated content",
                "version": 1
            },
            headers=self.headers
        )
        assert response.status_code == 200
        updated_data = response.json()
        assert updated_data["title"] == "Updated Title"
        assert updated_data["version"] == 2
        
        # Try to update with old version (should fail)
        response = client.put(f"/notes/{note_id}", 
            json={
                "title": "Another Update",
                "content": "Another content",
                "version": 1  # Old version
            },
            headers=self.headers
        )
        assert response.status_code == 409  # Conflict
