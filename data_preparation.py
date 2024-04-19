import os
import shutil
import random

# Step 1: Set the paths for your original dataset and test dataset
original_dataset_path = "./dataset/emotion/train"
test_data_path = "./dataset/emotion/test"

# Step 2: Create the test dataset directory if it doesn't exist
os.makedirs(test_data_path, exist_ok=True)

# Step 3: List emotions in the original dataset
emotions = os.listdir(original_dataset_path)

# Step 4: Copy a subset of images for each emotion to the test dataset
for emotion in emotions:
    image_files = os.listdir(os.path.join(original_dataset_path, emotion))

    # Select a subset of images (e.g., 100 images per emotion)
    test_samples = random.sample(image_files, min(100, len(image_files)))

    # Create emotion folders in the test dataset
    os.makedirs(os.path.join(test_data_path, emotion), exist_ok=True)

    # Copy selected images to the test dataset
    for sample in test_samples:
        src_path = os.path.join(original_dataset_path, emotion, sample)
        dest_path = os.path.join(test_data_path, emotion, sample)
        shutil.copy(src_path, dest_path)

# Print a message indicating the data preparation is complete
print("Test data preparation completed.")

