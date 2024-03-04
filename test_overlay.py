import cv2
import numpy as np

# Create a white window
window_width = 800
window_height = 600
window = 255 * np.ones((window_height, window_width, 3), dtype=np.uint8)

# Load the image
image = cv2.imread('screenshot.png', cv2.IMREAD_UNCHANGED)

# Resize the image to fit within the window
image = cv2.resize(image, (window_width, int(window_width * image.shape[0] / image.shape[1])))

# Get the dimensions of the resized image
image_height, image_width, _ = image.shape

# Calculate the position to place the image at the center top of the window
start_x = int((window_width - image_width) / 2)
start_y = 0

# Overlay the image on the window
window[start_y:start_y+image_height, start_x:start_x+image_width] = image

# Display the window
cv2.imshow('CV2 Window with Image Overlay', window)
cv2.waitKey(0)
cv2.destroyAllWindows()
