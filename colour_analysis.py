from PIL import Image
import numpy as np

def analyze_colors(image_path):
    # Open the image using Pillow
    image = Image.open(image_path)

    # Convert the image to a NumPy array for easy manipulation
    image_array = np.array(image)

    # Get the dimensions of the image
    height, width, _ = image_array.shape

    # Reshape the array to a list of RGB values
    rgb_values = image_array.reshape((height * width, 3))

    # Calculate the average color values
    average_color = np.mean(rgb_values, axis=0)

    return average_color
