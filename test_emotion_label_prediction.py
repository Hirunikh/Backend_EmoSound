# unit testing
import pytest
import numpy as np
from app import get_emotion_label

# Define test cases for different emotions
TEST_CASES = [
    (np.array([0.1, 0.2, 0.5, 0.1, 0.1]), 'Happy'),
    (np.array([0.2, 0.1, 0.3, 0.4, 0.0]), 'Neutral'),
    (np.array([0.4, 0.1, 0.2, 0.1, 0.2]), 'Angry'),
    (np.array([0.1, 0.5, 0.1, 0.1, 0.2]), 'Excited'),
    (np.array([0.3, 0.0, 0.1, 0.2, 0.4]), 'Sad')
]

@pytest.mark.parametrize("prediction, expected_emotion", TEST_CASES)
def test_get_emotion_label(prediction, expected_emotion):
    # Call the emotion label prediction function
    predicted_emotion = get_emotion_label(prediction)

    # Assert that the predicted emotion matches the expected emotion label
    assert predicted_emotion == expected_emotion


# Print a message indicating that the task has been fulfilled correctly
print("Unit tests for emotion label prediction passed successfully!")
