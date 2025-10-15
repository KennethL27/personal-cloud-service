import pytest

class TestAuthVerify:
    def test_verify_auth__success(self, test_client, bypass_auth):
        response = test_client.get("/auth/verify/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is True
        assert data["user"]["email"] == "test@gmail.com"

    def test_verify_auth__no_token(self, test_client):
        response = test_client.get("/auth/verify/")
        
        assert response.status_code == 401  
