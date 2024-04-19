import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from preprocessing import load_and_preprocess_data
from models.cnn_model import create_cnn_model, create_cnn_model_v2
from tensorflow import keras
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
import os  # Import the os module

# Set the path to your dataset
data_path = "./dataset/emotion/train"

# Load and preprocess the data
X_train, X_test, y_train, y_test = load_and_preprocess_data(data_path)

# Build the CNN model
input_shape = X_train[0].shape

num_classes = len(np.unique(y_train))
model = create_cnn_model_v2(input_shape, num_classes)

# Define EarlyStopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Define ReduceLROnPlateau callback
learning_rate_reduction = ReduceLROnPlateau(
    monitor='val_loss',
    patience=3,
    verbose=1,
    factor=0.5,
    min_lr=0.00001
)

# Train the model
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=20,
    batch_size=100,
    callbacks=[early_stopping, learning_rate_reduction]
)

# Get the absolute path of the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path to save the model
model_path = os.path.join(current_directory, 'emotion_model.h5')

# Save the trained model using the absolute path
model.save(model_path)

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Load the trained model
emotion_model = keras.models.load_model('emotion_model.h5')

# Compile the loaded model
emotion_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Create a DataFrame from the training history
history_df = pd.DataFrame(history.history)

# Plot the training and validation loss
history_df.loc[:, ['loss', 'val_loss']].plot()
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')

# Add text to the plot
# plt.text(0.06, 1.2, 'Adding 1 Dense and change Epoch', style='italic',
#         bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

# Display the plot
plt.show()
