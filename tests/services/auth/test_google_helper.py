import pytest
import os
from unittest.mock import patch, MagicMock
from src.services.auth.google_helper import verify_google_token

class TestGoogleHelper:
    def test_verify_google_token__success(self):
        mock_idinfo = {
            "email": "test@gmail.com",
            "name": "Test User",
            "picture": "https://example.com/picture.jpg",
            "sub": "google_user_id_123",
            "email_verified": True
        }
        
        with patch('src.services.auth.google_helper.id_token.verify_oauth2_token', return_value=mock_idinfo), \
             patch.dict(os.environ, {'GOOGLE_CLIENT_ID': 'test-client-id'}):
            
            result = verify_google_token("valid_token")
            
            assert result is not None
            assert result == mock_idinfo

    def test_verify_google_token__unverified_email(self):
        mock_idinfo = {
            "email": "test@gmail.com",
            "name": "Test User",
            "email_verified": False
        }
        
        with patch('src.services.auth.google_helper.id_token.verify_oauth2_token', return_value=mock_idinfo), \
             patch.dict(os.environ, {'GOOGLE_CLIENT_ID': 'test-client-id'}):
            
            result = verify_google_token("valid_token")
            assert result is None

    def test_verify_google_token__invalid_token(self):
        """Test verification with invalid token."""
        with patch('src.services.auth.google_helper.id_token.verify_oauth2_token', side_effect=ValueError("Invalid token")), \
             patch.dict(os.environ, {'GOOGLE_CLIENT_ID': 'test-client-id'}):
            
            result = verify_google_token("invalid_token")
            assert result is None

    def test_verify_google_token__missing_email(self):
        """Test token verification with missing email."""
        mock_idinfo = {
            "name": "Test User",
            "email_verified": True
            # Missing email field
        }
        
        with patch('src.services.auth.google_helper.id_token.verify_oauth2_token', return_value=mock_idinfo), \
             patch.dict(os.environ, {'GOOGLE_CLIENT_ID': 'test-client-id'}):
            
            result = verify_google_token("valid_token")
            assert result is not None
            assert result["email"] is None

    def test_verify_google_token__missing_client_id(self):
        """Test error when GOOGLE_CLIENT_ID is not set."""
        with patch('src.services.auth.google_helper.os.getenv', return_value=None):
            assert verify_google_token("valid_token") is None

    def test_verify_google_token__general_exception(self):
        """Test handling of general exceptions."""
        with patch('src.services.auth.google_helper.id_token.verify_oauth2_token', side_effect=Exception("General error")), \
             patch.dict(os.environ, {'GOOGLE_CLIENT_ID': 'test-client-id'}):
            
            result = verify_google_token("valid_token")
            assert result is None
