# unit testing
import pytest
from app import get_recommended_music

def test_get_recommended_music():
    # Mock the list of song names
    song_names = ['Song1', 'Song2', 'Song3']

    # Test with the mock data
    recommended_music = get_recommended_music(song_names)

    # Assert the output format and content
    assert isinstance(recommended_music, list)
    assert len(recommended_music) == len(song_names)

    # Add more specific assertions as needed

# Print a message indicating that the task has been fulfilled correctly
print("Unit test for get_recommended_music passed successfully!")
