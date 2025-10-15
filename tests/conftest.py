import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch

@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

@pytest.fixture
def mock_user():
    """Mock authenticated user for testing."""
    return {
        "email": "test@gmail.com",
        "name": "Test User",
        "picture": "https://example.com/picture.jpg",
        "sub": "google_user_id_123"
    }

@pytest.fixture
def auth_headers():
    """Mock authentication headers for testing."""
    return {"Cookie": "access_token=mock_jwt_token"}

@pytest.fixture
def authenticated_client(test_client, mock_user):
    """Test client with authentication mocked."""
    with patch('src.api.auth.dependencies.get_current_user', return_value=mock_user):
        yield test_client

@pytest.fixture
def bypass_auth():
    """Fixture to bypass authentication for existing tests."""
    from fastapi.testclient import TestClient
    from src.main import app
    from src.api.auth.dependencies import get_current_user
    
    def mock_get_current_user():
        return {
            "email": "test@gmail.com",
            "name": "Test User",
            "picture": "https://example.com/picture.jpg",
            "sub": "google_user_id_123"
        }
    
    # Override the dependency
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    yield mock_get_current_user
    
    # Clean up
    app.dependency_overrides.clear()