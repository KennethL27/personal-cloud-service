import pytest

class TestAuthLogout:
    def test_logout(self, test_client):
        response = test_client.post("/auth/logout/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Logout successful"
        
        # Check that cookie was cleared
        cookies = response.cookies
        assert "access_token" not in cookies or cookies.get("access_token") == ""
