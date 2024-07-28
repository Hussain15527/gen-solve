# File: png_processor.py

import numpy as np
import cv2
from scipy import ndimage
from skimage import measure

def test_ximgproc():
    """Test if the ximgproc module is available."""
    try:
        cv2.ximgproc
        print("ximgproc module is available.")
        return True
    except AttributeError:
        print("ximgproc module is not available. Please install opencv-contrib-python.")
        return False

def read_png(png_path):
    """Read a PNG image and return it as a grayscale numpy array."""
    image = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Failed to read image at {png_path}")
    return image

def preprocess_image(image):
    """Preprocess the image for edge detection."""
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
    return binary

def detect_edges(binary_image):
    """Detect edges in the binary image."""
    edges = cv2.Canny(binary_image, 50, 150)
    return edges

def thin_edges(edges):
    """Apply morphological thinning to the edges."""
    if not test_ximgproc():
        raise ImportError("ximgproc module is required for edge thinning.")
    thinned = cv2.ximgproc.thinning(edges)
    return thinned

def extract_polylines(thinned_edges):
    """Extract polylines from the thinned edges."""
    contours = measure.find_contours(thinned_edges, 0.5)
    return contours

def simplify_polyline(polyline, epsilon=1.0):
    """Simplify a polyline using the Douglas-Peucker algorithm."""
    return measure.approximate_polygon(polyline, tolerance=epsilon)

def png_to_polylines(png_path, epsilon=1.0):
    """Convert a PNG image to a list of polylines."""
    image = read_png(png_path)
    binary = preprocess_image(image)
    edges = detect_edges(binary)
    thinned = thin_edges(edges)
    polylines = extract_polylines(thinned)
    simplified_polylines = [simplify_polyline(polyline, epsilon) for polyline in polylines]
    return simplified_polylines

def save_polylines_to_csv(polylines, csv_path):
    """Save the polylines to a CSV file in the format expected by the regularization module."""
    with open(csv_path, 'w') as f:
        for i, polyline in enumerate(polylines):
            for j, point in enumerate(polyline):
                f.write(f"{i},{j},{point[0]},{point[1]}\n")

if __name__ == "__main__":
    test_ximgproc()