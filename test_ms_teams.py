import cv2
import mss
import numpy as np
from PIL import Image
import pygetwindow as gw

def capture_window(window_title):
    try:
        # Find the window with the specified title
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            win = windows[0]  # Get the first window with the given title
            window_bbox = {'top': win.top, 'left': win.left, 'width': win.width, 'height': win.height}
            
            with mss.mss() as sct:
                window_capture = sct.grab(window_bbox)
                window_img = Image.frombytes("RGB", window_capture.size, window_capture.bgra, "raw", "BGRX")
                return np.array(window_img), win
        else:
            return None, None
    except Exception as e:
        print(f"Error capturing window: {e}")
        return None, None

# Example usage:
window_title = "Microsoft Teams"
window_img, window_obj = capture_window(window_title)
if window_img is not None:
    # Do something with the captured image
    pass

# Step 1: Capture the Full Monitor Screen
with mss.mss() as sct:
    monitor_number = 1  # Adjust this number to select the correct monitor
    mon = sct.monitors[monitor_number]
    monitor = {
        "top": mon["top"],
        "left": mon["left"],
        "width": mon["width"],
        "height": mon["height"],
        "mon": monitor_number,
    }
    monitor_screen = sct.grab(monitor)
    monitor_img = Image.frombytes("RGB", monitor_screen.size, monitor_screen.bgra, "raw", "BGRX")
    monitor_img = np.array(monitor_img)

# windows = gw.getAllTitles()
# print(windows)

# Step 2: Locate and Capture the Microsoft Teams Window
# teams_img, win = capture_window("Microsoft Teams")
teams_img, win = capture_window("Notion Calendar")

# Step 3: Overlay the Teams Window Capture onto the Monitor Capture
if teams_img is not None and win is not None:
    # Calculate the position where the window image should be placed
    x_offset = win.left - monitor["left"]
    y_offset = win.top - monitor["top"]
    
    # Overlay the Teams window onto the monitor image
    y1, y2 = y_offset, y_offset + teams_img.shape[0]
    x1, x2 = x_offset, x_offset + teams_img.shape[1]

    alpha_s = teams_img[:, :, 2] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        monitor_img[y1:y2, x1:x2, c] = (alpha_s * teams_img[:, :, c] +
                                        alpha_l * monitor_img[y1:y2, x1:x2, c])

# Convert back to BGR for OpenCV
monitor_img = cv2.cvtColor(monitor_img, cv2.COLOR_RGB2BGR)

# Display the result
cv2.imshow("Overlay", monitor_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Step 5: Save or Display the Result
cv2.imwrite('overlay_result.png', monitor_img)
