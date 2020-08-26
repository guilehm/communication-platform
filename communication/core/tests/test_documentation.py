class TestDocumentation:

    def test_documentation_redoc_response(self, client):
        response = client.get('/redoc/')
        assert response.status_code == 200

    def test_documentation_swagger_response(self, client):
        response = client.get('/swagger/')
        assert response.status_code == 200
