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
from multiprocessing import Process, Manager

import cProfile


class FPS:
    def __init__(self):
        self._start_time = time()
        self._frame_count = 0
        self.current_fps = "Calculating..."  # Change to indicate calculation on start

    def update(self):
        """Increment the frame count."""
        self._frame_count += 1
        self.calculate_fps()  # Move FPS calculation here for immediate feedback

    def calculate_fps(self):
        """Calculate and update FPS every second."""
        current_time = time()
        elapsed_time = current_time - self._start_time

        if elapsed_time >= 1.0:
            self.current_fps = round(self._frame_count / elapsed_time, 2)
            self._start_time = current_time
            self._frame_count = 0

    def add_to_frame(self, frame):
        """Display the FPS on the frame."""
        # Ensure FPS is a string for cases where it’s "Calculating..."
        fps_display = f"FPS: {self.current_fps}" if isinstance(self.current_fps, str) else f"FPS: {self.current_fps:.1f}"
        cv2.putText(frame, fps_display, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

# class FPS:
#     def __init__(self):
#         self.curr_time = time()

#     def get_fps(self):
#         curr_fps = round((1 / (0.000001 + time() - self.curr_time)), 1)
#         self.curr_time = time()
#         return curr_fps

#     def add_fps_to_image(self, img, fps):
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         text_location = (30, 40)  # Adjust based on your capture area
#         font_scale = 1
#         font_color = (0, 255, 0)  # Green for better visibility
#         thickness = 2
#         line_type = 2

#         # Display the FPS text
#         cv2.putText(img, f"FPS: {fps}", text_location, font, font_scale, font_color, thickness, line_type)


class FrameCounter:
    def __init__(self, interval_frames):
        self.interval_frames = interval_frames
        self.frame_count = 0

    def is_time_to_operate(self):
        self.frame_count += 1
        if self.frame_count >= self.interval_frames:
            self.frame_count = 0  # Reset the counter
            return True
        return False

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

def capture_frames(monitor, shared_frame_data):
    sct = mss.mss()

    while True:
        img = sct.grab(monitor)
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
        shared_frame_data['frame'] = frame


def calculate_dominant_colors(shared_frame_data, color_smoother, frame_counter):
    while True:
        frame = shared_frame_data['frame']

        if frame is not None and frame_counter.is_time_to_operate():
            # Assuming kmeans_get_colours now returns three dominant colors
            dominant_colors = kmeans_get_colours(frame, K=3)
            color_smoother.add_colors(dominant_colors)
            smooth_colors = color_smoother.get_average_colors()

            shared_frame_data['smooth_colors'] = smooth_colors

def create_radial_gradient(center_color, mid_color, outer_color, image_size):
    # Generate a grid of coordinates (x, y)
    x = np.linspace(-1, 1, image_size[0])
    y = np.linspace(-1, 1, image_size[1])
    xv, yv = np.meshgrid(x, y)

    # Calculate distance from the center for each point
    dist = np.sqrt(xv**2 + yv**2)

    # Normalize distances to be in the range [0, 1]
    max_dist = np.sqrt(2)
    dist_normalized = dist / max_dist

    # Create masks for different regions
    center_mask = dist_normalized <= 1/3
    mid_mask = (dist_normalized > 1/3) & (dist_normalized <= 2/3)
    outer_mask = dist_normalized > 2/3

    # Preallocate an image array
    gradient_image = np.zeros((*image_size, 3), dtype=np.float32)

    # Apply colors based on the distance
    # For a smoother blend, you would adjust the blending based on the distance
    # Here, we're just assigning colors to demonstrate the approach
    gradient_image[center_mask] = center_color
    gradient_image[mid_mask] = mid_color
    gradient_image[outer_mask] = outer_color

    # Blend colors (simple linear blend for demonstration)
    # Calculate blend factors for mid and outer regions
    blend_factor_mid = (dist_normalized[mid_mask] - 1/3) / (1/3)
    blend_factor_outer = (dist_normalized[outer_mask] - 2/3) / (1/3)

    # Calculate blended colors
    gradient_image[mid_mask] = (1 - blend_factor_mid[:, None]) * center_color + blend_factor_mid[:, None] * mid_color
    gradient_image[outer_mask] = (1 - blend_factor_outer[:, None]) * mid_color + blend_factor_outer[:, None] * outer_color

    return np.clip(gradient_image, 0, 255).astype(np.uint8)

def main():
    with Manager() as manager:
        shared_frame_data = manager.dict()
        shared_frame_data['frame'] = None
        shared_frame_data['smooth_colors'] = None

        fps_counter = FPS()

        monitor_number = 1
        sct = mss.mss()

        mon = mss.mss().monitors[monitor_number]

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

        color_smoother = MultiColorExponentialMovingAverage(alpha=0.3, num_colors=3)

        frame_counter = FrameCounter(interval_frames=30)  # For example, every 30 frames

        frame_capture_process = Process(target=capture_frames, args=(monitor, shared_frame_data))
        # Pass frame_counter to the color calculation process
        color_calculation_process = Process(target=calculate_dominant_colors, args=(shared_frame_data, color_smoother, frame_counter))

        pr = cProfile.Profile()
        pr.enable()

        frame_capture_process.start()
        color_calculation_process.start()


        try:
            while True:
                frame = shared_frame_data['frame']
                smooth_colors = shared_frame_data['smooth_colors']

                if frame is not None and smooth_colors is not None:
                    frame_width = frame.shape[1]

                    color_blocks = [np.full((100, frame_width // 3, 3), color, dtype=np.uint8) for color in smooth_colors]

                    if sum(block.shape[1] for block in color_blocks) < frame_width:
                        gap = frame_width - sum(block.shape[1] for block in color_blocks)
                        last_block_width = color_blocks[-1].shape[1] + gap
                        color_blocks[-1] = np.full((100, last_block_width, 3), smooth_colors[-1], dtype=np.uint8)

                    color_row = np.hstack(color_blocks)
                    fps_counter.update()
                    fps_counter.add_to_frame(frame)

                    # gradient = create_radial_gradient(smooth_colors[0], smooth_colors[1], smooth_colors[2], (frame_width, 100))

                    # out = np.vstack([frame, color_row, gradient])

                    out = np.vstack([frame, color_row])

                    cv2.imshow("Screen Capture", out)

                if cv2.waitKey(25) & 0xFF == ord("q"):
                    frame_capture_process.terminate()
                    color_calculation_process.terminate()
                    cv2.destroyAllWindows()
                    break

        finally:
            frame_capture_process.join()
            color_calculation_process.join()

            pr.disable()

            # Print profiling results
            print("gi")
            pr.print_stats(sort='cumulative')
            pr.dump_stats('profile_results.prof')



if __name__ == '__main__':
    main()
