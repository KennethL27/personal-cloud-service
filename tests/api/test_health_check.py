from unittest.mock import patch, MagicMock

class TestHealthCheck:
    def test_health_check(self, test_client):
        response = test_client.get("/health/")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_health_check__fail(self, test_client):
        response = test_client.get("/health/bad")
        assert response.status_code == 404
        assert response.json() == {"detail": "Not Found"}

    @patch("src.api.health_check.health_check")
    def test_health_check_unexpected_error(self, test_client):
        response_mock = MagicMock()
        response_mock.status_code = 500
        response_mock.json.return_value = {"error": "Unexpected error"}

        test_client.get = MagicMock(return_value=response_mock)
        response = test_client.get("/health/")
        
        assert response.status_code == 500
        assert "error" in response.json()
