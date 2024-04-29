import numpy as np
from sklearn.metrics import classification_report, accuracy_score
from preprocessing import load_and_preprocess_data
from tensorflow import keras
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def evaluate_model(model, X_test, y_test):
    try:
        # Evaluate the model on the test set
        y_pred = model.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)

        # Print classification report and accuracy
        logging.info("Classification Report:")
        logging.info(classification_report(y_test, y_pred_classes, zero_division=1))  # Set zero_division=1

        accuracy = accuracy_score(y_test, y_pred_classes)
        logging.info(f"Accuracy: {accuracy * 100:.2f}%")
    except Exception as e:
        logging.error(f'Error during model evaluation: {str(e)}')

if __name__ == "__main__":
    # Load and preprocess the test data
    test_data_path = "./dataset/emotion/test"
    X_train, X_test, y_train, y_test = load_and_preprocess_data(test_data_path)

    # Load the trained model
    model = keras.models.load_model('emotion_model.h5')

    # Compile the loaded model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Evaluate the model on the test data
    evaluate_model(model, X_test, y_test)
