import pytest
import os
from unittest.mock import patch
from src.services.auth.allow_email_helper import is_email_allowed

class TestAllowEmailHelper:
    def setup_method(self, method):
        import src.services.auth.allow_email_helper as helper
        helper._cached_allowed_emails_set = None

    def test_is_email_allowed__true(self):
        with patch.dict(os.environ, {'ALLOWED_EMAILS': "[\"user1@gmail.com\",\"user2@gmail.com\"]"}):
            assert is_email_allowed('user1@gmail.com') is True
            assert is_email_allowed('USER1@GMAIL.COM') is True

    def test_is_email_allowed__false(self):
        with patch.dict(os.environ, {'ALLOWED_EMAILS': "[\"user1@gmail.com\"]"}):
            assert is_email_allowed('user2@gmail.com') is False
            assert is_email_allowed('') is False
            assert is_email_allowed(None) is False

    def test_is_email_allowed__missing_env_var(self):
        with patch('os.getenv', return_value=None):
            with pytest.raises(ValueError, match="ALLOWED_EMAILS environment variable not set"):
                is_email_allowed('user1@gmail.com')

    def test_is_email_allowed__invalid_json(self):
        with patch.dict(os.environ, {'ALLOWED_EMAILS': '["invalid json"'}):
            with pytest.raises(ValueError, match="ALLOWED_EMAILS environment variable is not valid JSON"):
                is_email_allowed('user@gmail.com')
    
    def test_is_email_allowed__non_list_json(self):
        with patch.dict(os.environ, {'ALLOWED_EMAILS': '"not-a-list"'}):
            with pytest.raises(ValueError, match="ALLOWED_EMAILS environment variable must be a JSON list"):
                is_email_allowed('user@gmail.com')

    def test_is_email_allowed__non_string_emails(self):
        with patch.dict(os.environ, {'ALLOWED_EMAILS': '["user@gmail.com", 123, null, true]'}):
            assert is_email_allowed('user@gmail.com') is True
            assert is_email_allowed('nonexistent@gmail.com') is False

    def test_is_email_allowed__caching(self):
        with patch.dict(os.environ, {'ALLOWED_EMAILS': '["user@gmail.com"]'}):
            assert is_email_allowed('user@gmail.com') is True
            
            with patch('os.getenv', return_value=None):
                assert is_email_allowed('user@gmail.com') is True

    def test_is_email_allowed__edge_cases(self):
        with patch.dict(os.environ, {'ALLOWED_EMAILS': '["test@example.com", "user@domain.org"]'}):
            # Test various email formats
            assert is_email_allowed('TEST@EXAMPLE.COM') is True
            assert is_email_allowed('test@example.com') is True
            assert is_email_allowed('different@domain.com') is False