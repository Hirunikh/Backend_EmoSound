import os
import matplotlib.pyplot as plt
from tensorflow import keras
from keras.preprocessing import image
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to plot digit distribution
def plot_digit_distribution(data_path):
    try:
        logging.info('Plotting digit distribution.')
        emotions = os.listdir(data_path)
        counts = [len(os.listdir(os.path.join(data_path, emotion))) for emotion in emotions]

        # Plot the distribution of images per emotion
        plt.bar(emotions, counts)
        plt.title('Digit Distribution')
        plt.xlabel('Emotion')
        plt.ylabel('Count')
        plt.show()

    except Exception as e:
        logging.error(f'Error in plotting digit distribution: {str(e)}')

# Function to visualize sample images
def visualize_data(data_path, num_samples=5):
    try:
        logging.info('Visualizing sample images.')
        emotions = os.listdir(data_path)

        for emotion in emotions:
            image_files = os.listdir(os.path.join(data_path, emotion))[:num_samples]

            # Create a figure to display sample images for the current emotion
            plt.figure(figsize=(10, 2))
            for i, image_file in enumerate(image_files):
                img_path = os.path.join(data_path, emotion, image_file)
                img = image.load_img(img_path, target_size=(64, 64))
                plt.subplot(1, num_samples, i + 1)
                plt.imshow(img)
                plt.title(emotion)
                plt.axis('off')
            plt.show()

    except Exception as e:
        logging.error(f'Error in visualizing sample images: {str(e)}')


if __name__ == "__main__":
    test_data_path = "./dataset/emotion/test"

    # Visualize digit distribution
    plot_digit_distribution(test_data_path)

    # Visualize sample images
    visualize_data(test_data_path)
