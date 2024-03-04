import cv2
import numpy as np

def create_radial_gradient(center_color, mid_color, outer_color, image_size):
    """
    Create an image with a radial gradient with three colors.
    """
    # Create an empty black image
    image = np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)

    # Calculate the center of the image
    center_x, center_y = image_size[0] // 2, image_size[1] // 2

    # Maximum distance from the center to a corner
    max_dist = np.sqrt(center_x**2 + center_y**2)

    for y in range(image_size[1]):
        for x in range(image_size[0]):
            # Calculate distance to the center
            dist = np.sqrt((center_x - x)**2 + (center_y - y)**2)

            # Normalize the distance
            normalized_dist = dist / max_dist

            if normalized_dist <= 0.33:
                # Closer to the center
                blend_color = center_color
            elif normalized_dist <= 0.66:
                # Middle region - blend center and mid color based on distance
                blend_factor = (normalized_dist - 0.33) / 0.33
                blend_color = (1 - blend_factor) * np.array(center_color) + blend_factor * np.array(mid_color)
            else:
                # Outer region - blend mid and outer color based on distance
                blend_factor = (normalized_dist - 0.66) / 0.34
                blend_color = (1 - blend_factor) * np.array(mid_color) + blend_factor * np.array(outer_color)

            # Assign the blend color to the current pixel
            image[y, x] = blend_color

    return image.astype(np.uint8)

# Define your colors in BGR format
center_color = [0, 255, 255]  # Yellow
mid_color = [255, 0, 0]       # Blue
outer_color = [0, 255, 0]     # Green

# Image size (width, height)
image_size = (600, 400)

# Create the gradient image
gradient_image = create_radial_gradient(center_color, mid_color, outer_color, image_size)

# Display the image
cv2.imshow('Radial Gradient', gradient_image)
cv2.waitKey(0)
cv2.destroyAllWindows()