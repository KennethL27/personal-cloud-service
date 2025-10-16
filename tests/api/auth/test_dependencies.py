import pytest
from unittest.mock import patch
from fastapi import HTTPException, status, Cookie
from src.api.auth.dependencies import (
    create_unauthorized_exception,
    create_forbidden_exception,
    get_current_user
)

class TestAuthDependencies:
    def test_create_unauthorized_exception(self):
        detail = "Test unauthorized message"
        exception = create_unauthorized_exception(detail)
        
        assert isinstance(exception, HTTPException)
        assert exception.status_code == status.HTTP_401_UNAUTHORIZED
        assert exception.detail == detail
        assert exception.headers["WWW-Authenticate"] == "Bearer"

    def test_create_forbidden_exception(self):
        detail = "Test forbidden message"
        exception = create_forbidden_exception(detail)
        
        assert isinstance(exception, HTTPException)
        assert exception.status_code == status.HTTP_403_FORBIDDEN
        assert exception.detail == detail

    @pytest.mark.asyncio
    async def test_get_current_user__no_token(self):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(None)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Not authenticated"

    @pytest.mark.asyncio
    async def test_get_current_user__invalid_token(self):
        with patch('src.api.auth.dependencies.verify_token', return_value=None):
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user("invalid_token")
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Invalid authentication credentials"

    @pytest.mark.asyncio
    async def test_get_current_user__missing_email_in_payload(self):
        mock_payload = {"name": "Test User", "exp": 1234567890}
        
        with patch('src.api.auth.dependencies.verify_token', return_value=mock_payload):
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user("valid_token")
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Invalid token payload"

    @pytest.mark.asyncio
    async def test_get_current_user__email_not_allowed(self):
        mock_payload = {
            "sub": "unauthorized@gmail.com",
            "name": "Unauthorized User",
            "picture": "https://example.com/picture.jpg"
        }
        
        with patch('src.api.auth.dependencies.verify_token', return_value=mock_payload), \
             patch('src.api.auth.dependencies.is_email_allowed', return_value=False):
            
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user("valid_token")
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert exc_info.value.detail == "Your email is not authorized to access this service"

    @pytest.mark.asyncio
    async def test_get_current_user__success_with_minimal_payload(self):
        mock_payload = {
            "sub": "test@gmail.com"
        }
        
        with patch('src.api.auth.dependencies.verify_token', return_value=mock_payload), \
             patch('src.api.auth.dependencies.is_email_allowed', return_value=True):
            
            user = await get_current_user("valid_token")
            
            assert user["email"] == "test@gmail.com"
            assert user["name"] is None
            assert user["sub"] == "test@gmail.com"
            assert user["picture"] is None

    @pytest.mark.asyncio
    async def test_get_current_user__success_with_full_payload(self):
        mock_payload = {
            "sub": "test@gmail.com",
            "name": "Test User",
            "picture": "https://example.com/picture.jpg"
        }
        
        with patch('src.api.auth.dependencies.verify_token', return_value=mock_payload), \
             patch('src.api.auth.dependencies.is_email_allowed', return_value=True):
            
            user = await get_current_user("valid_token")
            
            assert user["email"] == "test@gmail.com"
            assert user["name"] == "Test User"
            assert user["picture"] == "https://example.com/picture.jpg"
            assert user["sub"] == "test@gmail.com"