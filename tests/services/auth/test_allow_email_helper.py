import pytest
import os
from unittest.mock import patch
from src.services.auth.allow_email_helper import is_email_allowed

class TestAllowEmailHelper:
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
        with patch.object(os.environ, 'get', return_value=None):
            with pytest.raises(ValueError, match="ALLOWED_EMAILS environment variable not set"):
                is_email_allowed('user1@gmail.com')
