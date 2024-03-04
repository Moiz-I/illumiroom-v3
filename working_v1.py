'''
IDEAS
- multiple processes for each
- less frquenctly, e.g. check dominant color every 5 frames
- also look into light sync devices how they check for color
'''
import cv2
import numpy as np
import mss
from time import time
from cv2 import putText, FONT_HERSHEY_SIMPLEX
from colorthief import ColorThief
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import colorsys



class FPS:
    def __init__(self):
        self.curr_time = time()

    def get_fps(self):
        curr_fps = round((1 / (0.000001 + time() - self.curr_time)), 1)
        self.curr_time = time()
        return curr_fps

    def add_fps_to_image(self, img, fps):
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_location = (30, 40)  # Adjust based on your capture area
        font_scale = 1
        font_color = (0, 255, 0)  # Green for better visibility
        thickness = 2
        line_type = 2

        # Display the FPS text
        cv2.putText(img, f"FPS: {fps}", text_location, font, font_scale, font_color, thickness, line_type)


class MultiColorExponentialMovingAverage:
    def __init__(self, alpha=0.01, num_colors=3):
        self.alpha = alpha
        self.num_colors = num_colors
        self.average_colors = [None] * num_colors
    
    def add_colors(self, colors):
        for i in range(self.num_colors):
            if self.average_colors[i] is None:
                self.average_colors[i] = np.array(colors[i], dtype=np.float32)
            else:
                self.average_colors[i] = self.alpha * np.array(colors[i], dtype=np.float32) + (1 - self.alpha) * self.average_colors[i]
    
    def get_average_colors(self):
        return [np.uint8(c).tolist() for c in self.average_colors]


def get_dominant_color(frame):
    # Convert the OpenCV frame to a PIL Image
    pil_image = Image.fromarray(frame)

    # Save the PIL Image to a BytesIO object
    f = BytesIO()
    pil_image.save(f, format='JPEG')

    # Move the pointer of BytesIO object to the start
    f.seek(0)

    # Pass the BytesIO object to ColorThief
    color_thief = ColorThief(f)

    # Extract the dominant color
    dominant_color = color_thief.get_color(quality=1)
    print(dominant_color)


def kmeans_get_colours(frame, K=3):
    # Convert image to data (resize to reduce complexity)
    pixels = cv2.resize(frame, (100, 100)).reshape((-1, 3))

    sample_fraction = 1
    # Sample a fraction of the pixels randomly
    num_pixels = len(pixels)
    sampled_pixels = pixels[np.random.choice(num_pixels, int(num_pixels * sample_fraction), replace=False)]

    # Convert to np.float32
    sampled_pixels = np.float32(sampled_pixels)

    # Define criteria and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(sampled_pixels, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert centers to integers
    centers = np.uint8(centers)

    # Identify the three most dominant colors based on the cluster sizes
    cluster_sizes = np.bincount(labels.flatten())
    dominant_idxs = np.argsort(-cluster_sizes)[:K]  # Get indexes of K largest clusters
    
    # Extract the colors corresponding to these indexes
    dominant_colors = centers[dominant_idxs].tolist()

    return dominant_colors

def is_blue(h,s,v):
    return h > 180 and h < 255 and s > 50 and v > 30

def rgb_to_hsv(rgb):
    b, g, r = rgb
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    h = int(h * 360)  # Convert hue to degrees
    s = int(s * 100)  # Convert saturation to percentage
    v = int(v * 100)  # Convert value to percentage
    isBlue = is_blue(h,s,v)
    print("is blue: ", is_blue(h,s,v))
    return isBlue
    # return f"hsv({h}, {s}%, {v}%)"

def main():
    # Create an FPS counter instance
    fps_counter = FPS()

    # Create an mss instance
    sct = mss.mss()

    # Monitor settings (adjust as needed)
    monitor_number = 1
    mon = sct.monitors[monitor_number]
    capture_width = 400
    capture_height = 300

    monitor = {
        "top": 100,
        "left": mon["width"] - capture_width,
        "width": capture_width,
        "height": capture_height,
        "mon": monitor_number,
    }

    # Initialize the ThreadPoolExecutor
    # executor = ThreadPoolExecutor(max_workers=1)

    color_smoother = MultiColorExponentialMovingAverage(alpha=0.3, num_colors=3)
    while True:
        img = sct.grab(monitor)
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)

        # Submit the color extraction task to the executor
        # future = executor.submit(get_dominant_color, frame)
        # dominant_color = color_thief.get_color(quality=1)
        # print(dominant_color)
        

        # Assuming kmeans_get_colours now returns three dominant colors
        dominant_colors = kmeans_get_colours(frame, K=3)  # Ensure this function returns three dominant colors
        color_smoother.add_colors(dominant_colors)
        smooth_colors = color_smoother.get_average_colors()
        # colors_hsv = [rgb_to_hsv(rgb) for rgb in smooth_colors]
        # print(colors_hsv)
        isBlue0 = rgb_to_hsv(smooth_colors[0])
        if isBlue0:
            #add "blue" to the screen
            # putText(frame, "blue", (50, 50), FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            putText(frame, "Blue detected!!!", (100, 100), FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)
        

        
        # Assuming frame.shape[1] is the width of the frame
        frame_width = frame.shape[1]

        # Create an image to display the smoothed colors
        # Ensure that the total width of color_blocks matches the frame's width exactly
        color_blocks = [np.full((100, frame_width // 3, 3), color, dtype=np.uint8) for color in smooth_colors]

        # Adjust the last block's width if necessary to fill any gap
        if sum(block.shape[1] for block in color_blocks) < frame_width:
            # Calculate the gap and adjust the last block's width
            gap = frame_width - sum(block.shape[1] for block in color_blocks)
            last_block_width = color_blocks[-1].shape[1] + gap
            color_blocks[-1] = np.full((100, last_block_width, 3), smooth_colors[-1], dtype=np.uint8)

        color_row = np.hstack(color_blocks)

        # Calculate and display FPS
        fps = fps_counter.get_fps()
        fps_counter.add_fps_to_image(frame, fps)

        # Now, color_row should have the exact same width as frame, and stacking should work
        out = np.vstack([frame, color_row])

        # sf = frame.shape[1] / palette.shape[1]
        # out = np.vstack([frame, cv2.resize(palette, (0, 0), fx=sf, fy=sf)])

        cv2.imshow("Screen Capture", out)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

    # Shutdown the executor
    # executor.shutdown(wait=True)


if __name__ == '__main__':
    main()
