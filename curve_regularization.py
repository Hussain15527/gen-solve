
import numpy as np
from scipy import optimize
import cv2
import os

def read_csv(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    if os.path.getsize(csv_path) == 0:
        raise ValueError(f"CSV file is empty: {csv_path}")

    try:
        np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
        if np_path_XYs.ndim < 2:
            raise ValueError("CSV data has incorrect dimensions. Expected 2D array.")
        
        path_XYs = []
        for i in np.unique(np_path_XYs[:, 0]):
            npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
            XYs = []
            for j in np.unique(npXYs[:, 0]):
                XY = npXYs[npXYs[:, 0] == j][:, 1:]
                XYs.append(XY)
            path_XYs.append(XYs)
        return path_XYs
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {str(e)}")

def distance_point_line(point, line_params):
    a, b, c = line_params
    x, y = point
    return abs(a*x + b*y + c) / np.sqrt(a**2 + b**2)

def fit_line(points):
    x = points[:, 0]
    y = points[:, 1]
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    a, b, c = m, -1, c
    return a, b, c

def is_straight_line(points, threshold=0.1):
    if len(points) < 2:
        return False
    line_params = fit_line(points)
    distances = [distance_point_line(point, line_params) for point in points]
    return np.max(distances) < threshold

def distance_point_circle(point, circle_params):
    xc, yc, r = circle_params
    x, y = point
    return abs(np.sqrt((x - xc)**2 + (y - yc)**2) - r)

def fit_circle(points):
    def circle_error(params, points):
        return [distance_point_circle(point, params) for point in points]
    
    x_mean, y_mean = np.mean(points, axis=0)
    r_init = np.mean(np.sqrt(np.sum((points - [x_mean, y_mean])**2, axis=1)))
    params_init = [x_mean, y_mean, r_init]
    
    params_optimized, _ = optimize.leastsq(circle_error, params_init, args=(points,))
    return params_optimized

def is_circle(points, threshold=0.1):
    if len(points) < 3:
        return False
    circle_params = fit_circle(points)
    distances = [distance_point_circle(point, circle_params) for point in points]
    return np.max(distances) < threshold

def distance_point_ellipse(point, ellipse_params):
    x, y = point
    xc, yc, a, b, theta = ellipse_params
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    x_rotated = (x - xc) * cos_theta + (y - yc) * sin_theta
    y_rotated = -(x - xc) * sin_theta + (y - yc) * cos_theta
    return np.abs(((x_rotated ** 2) / (a ** 2)) + ((y_rotated ** 2) / (b ** 2)) - 1)

def fit_ellipse(points):
    ellipse = cv2.fitEllipse(points.astype(np.float32))
    center, axes, angle = ellipse
    return (*center, axes[0]/2, axes[1]/2, np.radians(angle))

def is_ellipse(points, threshold=0.1):
    if len(points) < 5:  # Ellipse fitting requires at least 5 points
        return False
    try:
        ellipse_params = fit_ellipse(points)
        distances = [distance_point_ellipse(point, ellipse_params) for point in points]
        return np.max(distances) < threshold
    except:
        return False

def distance_point_rectangle(point, rectangle_params):
    x, y = point
    cx, cy, width, height, angle = rectangle_params
    cos_angle, sin_angle = np.cos(angle), np.sin(angle)
    x_rotated = cos_angle * (x - cx) - sin_angle * (y - cy)
    y_rotated = sin_angle * (x - cx) + cos_angle * (y - cy)
    dx = np.abs(x_rotated) - width / 2
    dy = np.abs(y_rotated) - height / 2
    return max(dx, dy)

def fit_rectangle(points):
    rect = cv2.minAreaRect(points.astype(np.float32))
    center, (width, height), angle = rect
    return (*center, width, height, np.radians(angle))

def is_rectangle(points, threshold=0.1):
    if len(points) < 4:  # Rectangle fitting requires at least 4 points
        return False
    rectangle_params = fit_rectangle(points)
    distances = [distance_point_rectangle(point, rectangle_params) for point in points]
    return np.max(distances) < threshold

def regularize_curve(points):
    if is_straight_line(points):
        return {"type": "line", "params": fit_line(points), "points": points}
    elif is_circle(points):
        return {"type": "circle", "params": fit_circle(points), "points": points}
    elif is_ellipse(points):
        return {"type": "ellipse", "params": fit_ellipse(points), "points": points}
    elif is_rectangle(points):
        return {"type": "rectangle", "params": fit_rectangle(points), "points": points}
    else:
        return {"type": "unknown", "params": None, "points": points}

def process_paths(paths):
    regularized_paths = []
    for path in paths:
        regularized_path = []
        for curve in path:
            regularized_curve = regularize_curve(curve)
            regularized_path.append(regularized_curve)
        regularized_paths.append(regularized_path)
    return regularized_paths
