
#  client is the TestClient instance from the FastAPI app, as provided by the client fixture
#  in conftest.py. It simulates HTTP requests to the app’s endpoints in a controlled testing 
# environment.

def test_get_books(client):
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)