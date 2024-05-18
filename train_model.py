import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from preprocessing import load_and_preprocess_data
from models.cnn_model import create_cnn_model, create_cnn_model_v2, create_cnn_model_lite
from tensorflow import keras
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.src.legacy.preprocessing.image import ImageDataGenerator
import os  # Import the os module

# Set the path to your dataset
data_path = "./dataset/emotion/train"

# Load and preprocess the data
X_train, X_test, y_train, y_test = load_and_preprocess_data(data_path)

# Build the CNN model
input_shape = X_train[0].shape

num_classes = len(np.unique(y_train))
model = create_cnn_model_lite(input_shape, num_classes)

# Define EarlyStopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Define ReduceLROnPlateau callback
learning_rate_reduction = ReduceLROnPlateau(
    monitor='val_loss',
    patience=2,
    verbose=1,
    factor=0.5,
    min_lr=0.00001
)

epochs = 100
batch_size = 16

train_datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Train the model
history = model.fit(train_datagen.flow(X_train, y_train, batch_size=batch_size),
    validation_data=(X_test, y_test),
    epochs=epochs,
    callbacks=[early_stopping, learning_rate_reduction]
)

# Save the trained model using the absolute path
model.save('emotion_model_lite.h5')

# Create a DataFrame from the training history
history_df = pd.DataFrame(history.history)

# Plot the training and validation loss
history_df.loc[:, ['loss', 'val_loss']].plot()
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')

# Display the plot
plt.savefig('./captured-images/emotion_model_lite.jpg')
plt.show()
