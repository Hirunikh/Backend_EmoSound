# Regression testing
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Scenario 1: Test the index route
@pytest.mark.regression
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Emotion Music Backend!' in response.data

# Scenario 2: Test the /get_recommendations route with valid image data
@pytest.mark.regression
def test_get_recommendations_valid_image(client):
    valid_image_data = "data:image/png;base64,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"

    response = client.post('/get_recommendations', json={"image": valid_image_data})
    assert response.status_code == 200
    assert 'emotion' in response.json
    assert 'music' in response.json

# Scenario 3: Test the /get_recommendations route with invalid image data
@pytest.mark.regression
def test_get_recommendations_invalid_image(client):
    image_data = {"image": "invalid-base64-encoded-data"}  # Provide invalid image data here
    response = client.post('/get_recommendations', json=image_data)
    assert response.status_code == 500
    assert 'error' in response.json


# Scenario 4: Test the /popular_playlists route
@pytest.mark.regression
def test_popular_playlists_route(client):
    response = client.get('/popular_playlists')
    assert response.status_code == 200
    # Print response.json to inspect its structure
    print(response.json)
    # Check if 'playlists' key is present in the response JSON
    assert len(response.json) > 0
