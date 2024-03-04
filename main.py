from mss import mss
from colour_analysis import analyze_colors

# Save a screenshot of the 1st monitor
with mss() as sct:
    sct.shot(output='screenshot.png')

# Perform color analysis on the screenshot
screenshot_path = 'screenshot.png'
average_color = analyze_colors(screenshot_path)

print(f'Average Color: {average_color}')

import numpy as np
from PIL import Image

def palette(img):
    """
    Return palette in descending order of frequency
    """
    arr = np.asarray(img)
    palette, index = np.unique(asvoid(arr).ravel(), return_inverse=True)
    palette = palette.view(arr.dtype).reshape(-1, arr.shape[-1])
    count = np.bincount(index)
    order = np.argsort(count)
    return palette[order[::-1]]

def asvoid(arr):
    """View the array as dtype np.void (bytes)
    This collapses ND-arrays to 1D-arrays, so you can perform 1D operations on them.
    http://stackoverflow.com/a/16216866/190597 (Jaime)
    http://stackoverflow.com/a/16840350/190597 (Jaime)
    Warning:
    >>> asvoid([-0.]) == asvoid([0.])
    array([False], dtype=bool)
    """
    arr = np.ascontiguousarray(arr)
    return arr.view(np.dtype((np.void, arr.dtype.itemsize * arr.shape[-1])))


img = Image.open(screenshot_path, "r").convert('RGB')
print(palette(img)[:3])