import numpy as np
from sklearn.metrics import classification_report, accuracy_score
from preprocessing import load_and_preprocess_data
from tensorflow import keras

def evaluate_model(model, X_test, y_test):
    # Evaluate the model on the test set
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)

    # Print classification report and accuracy
    print("Classification Report:")
    print(classification_report(y_test, y_pred_classes, zero_division=1))  # Set zero_division=1

    accuracy = accuracy_score(y_test, y_pred_classes)
    print(f"Accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    # Load and preprocess the test data
    test_data_path = "./dataset/emotion/test"
    X_train, X_test, y_train, y_test = load_and_preprocess_data(test_data_path)

    # Build and train the model (as shown in the previous step)
    # model = create_cnn_model(input_shape=X_train[0].shape, num_classes=len(np.unique(y_train)))

    # Load the trained model
    model = keras.models.load_model('emotion_model.h5')

    # Compile the loaded model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Evaluate the model on the test data
    evaluate_model(model, X_test, y_test)
