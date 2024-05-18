import os
import numpy as np
from tensorflow import keras
from keras.preprocessing import image
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess_data(data_path):
    emotions = os.listdir(data_path)

    images = []
    labels = []

    for i, emotion in enumerate(emotions):
        image_files = os.listdir(os.path.join(data_path, emotion))

        for image_file in image_files:
            # Load the image and convert it to a numpy array
            img_path = os.path.join(data_path, emotion, image_file)
            img = image.load_img(img_path, target_size=(64, 64), color_mode="grayscale")
            img_array = image.img_to_array(img)
            images.append(img_array)
            labels.append(i)

    # Convert the lists to numpy arrays
    X = np.array(images)
    y = np.array(labels)

    # Normalize pixel values to be between 0 and 1
    X = X / 255.0

    # Perform label encoding
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    data_path = "./dataset/emotion/train"  # Adjust to your training dataset path

    # Load and preprocess the data
    X_train, X_test, y_train, y_test = load_and_preprocess_data(data_path)

    # Rest of your code, e.g., building and training the model

    # verify the shapes of the dataset
    print("Training data shape:", X_train.shape, y_train.shape)
    print("Testing data shape:", X_test.shape, y_test.shape)

