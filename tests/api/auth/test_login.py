import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

class TestAuthLogin:
    def test_login__success(self, test_client):
        mock_user_info = {
            "email": "test@gmail.com",
            "name": "Test User",
            "picture": "https://example.com/picture.jpg",
            "sub": "google_user_id_123",
            "email_verified": True
        }
        
        with patch('src.api.auth.login.verify_google_token', return_value=mock_user_info), \
             patch('src.api.auth.login.is_email_allowed', return_value=True), \
             patch('src.api.auth.login.create_access_token', return_value="mock_jwt_token"):
            
            response = test_client.post("/auth/login/", json={"token": "valid_google_token"})
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Login successful"
            assert data["user"]["email"] == "test@gmail.com"
            assert data["user"]["name"] == "Test User"
            
            # Check that cookie was set
            assert "access_token" in response.cookies

    def test_login__invalid_token(self, test_client):
        with patch('src.api.auth.login.verify_google_token', return_value=None):
            response = test_client.post("/auth/login/", json={"token": "invalid_token"})
            
            assert response.status_code == 401
            data = response.json()
            assert data["detail"] == "Invalid Google token"

    def test_login__email_not_verified(self, test_client):
        with patch('src.api.auth.login.verify_google_token', return_value=None):
            response = test_client.post("/auth/login/", json={"token": "valid_token"})
            
            assert response.status_code == 401
            data = response.json()
            assert data["detail"] == "Invalid Google token"

    def test_login__email_not_allowed(self, test_client):
        mock_user_info = {
            "email": "unauthorized@gmail.com",
            "name": "Unauthorized User",
            "email_verified": True
        }
        
        with patch('src.api.auth.login.verify_google_token', return_value=mock_user_info), \
             patch('src.api.auth.login.is_email_allowed', return_value=False):
            
            response = test_client.post("/auth/login/", json={"token": "valid_token"})
            
            assert response.status_code == 403
            data = response.json()
            assert data["detail"] == "Your email is not authorized to access this service"

    def test_login__missing_email(self, test_client):
        mock_user_info = {
            "name": "Test User",
            "email_verified": True
            # Missing email
        }
        
        with patch('src.api.auth.login.verify_google_token', return_value=mock_user_info):
            response = test_client.post("/auth/login/", json={"token": "valid_token"})
            
            assert response.status_code == 401
            data = response.json()
            assert data["detail"] == "Email not found in Google token"

    def test_login__missing_token_field(self, test_client):
        response = test_client.post("/auth/login/", json={})
        
        assert response.status_code == 422

    def test_login__invalid_json(self, test_client):
        response = test_client.post("/auth/login/", data="invalid json")
        
        assert response.status_code == 422
