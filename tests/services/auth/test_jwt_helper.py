import pytest
import os
from datetime import timedelta
from unittest.mock import patch
from src.services.auth.jwt_helper import create_access_token, verify_token, get_password_hash, verify_password

class TestJwtHelper:
    def test_create_access_token__success(self):
        data = {"sub": "test@example.com", "name": "Test User"}
        
        token = create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token__with_expires_delta(self):
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=30)
        
        token = create_access_token(data, expires_delta)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_token__success(self):
        data = {"sub": "test@example.com", "name": "Test User"}
        token = create_access_token(data)
        
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert payload["name"] == "Test User"

    def test_verify_token__invalid(self):
        invalid_token = "invalid.token.here"
        
        payload = verify_token(invalid_token)
        assert payload is None

    def test_verify_token__expired(self):
        data = {"sub": "test@example.com"}
        # Create token with very short expiration
        token = create_access_token(data, timedelta(seconds=-1))
        
        payload = verify_token(token)
        assert payload is None

    def test_get_password__hash(self):
        password = "testpass123"
        
        with patch('src.services.auth.jwt_helper.pwd_context.hash', return_value="hashed_password"):
            hashed = get_password_hash(password)
            
            assert isinstance(hashed, str)
            assert hashed == "hashed_password"
            assert hashed != password

    def test_verify_password__success(self):
        password = "testpass123"
        hashed = "hashed_password"
        
        with patch('src.services.auth.jwt_helper.pwd_context.verify', return_value=True):
            assert verify_password(password, hashed) is True

    def test_verify_password__failure(self):
        wrong_password = "wrongpass"
        hashed = "hashed_password"
        
        with patch('src.services.auth.jwt_helper.pwd_context.verify', return_value=False):
            assert verify_password(wrong_password, hashed) is False
