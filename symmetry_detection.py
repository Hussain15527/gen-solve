# File: symmetry_detection.py

import numpy as np
from scipy.spatial.distance import cdist

def find_reflection_symmetry(points, threshold=0.1):
    """
    Find reflection symmetry in a set of points.
    Returns the symmetry line parameters (a, b, c) where ax + by + c = 0.
    """
    center = np.mean(points, axis=0)
    centered_points = points - center

    best_symmetry = None
    best_score = float('inf')

    for angle in np.linspace(0, np.pi, 180):
        cos_theta, sin_theta = np.cos(angle), np.sin(angle)
        rotation_matrix = np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])
        
        rotated_points = np.dot(centered_points, rotation_matrix.T)
        flipped_points = rotated_points * [-1, 1]
        
        distances = cdist(rotated_points, flipped_points)
        min_distances = np.min(distances, axis=1)
        
        score = np.mean(min_distances)
        
        if score < best_score:
            best_score = score
            best_symmetry = (sin_theta, -cos_theta, -sin_theta*center[0] + cos_theta*center[1])

    return best_symmetry if best_score < threshold else None

def find_rotational_symmetry(points, threshold=0.1, max_order=8):
    """
    Find rotational symmetry in a set of points.
    Returns the order of rotational symmetry (2 for 180°, 3 for 120°, 4 for 90°, etc.).
    """
    center = np.mean(points, axis=0)
    centered_points = points - center

    best_order = 1
    best_score = float('inf')

    for order in range(2, max_order + 1):
        angle = 2 * np.pi / order
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        
        rotated_points = np.dot(centered_points, rotation_matrix.T)
        distances = cdist(centered_points, rotated_points)
        min_distances = np.min(distances, axis=1)
        
        score = np.mean(min_distances)
        
        if score < best_score:
            best_score = score
            best_order = order

    return best_order if best_score < threshold else 1

def detect_symmetry(regularized_curve):
    """
    Detect both reflection and rotational symmetry for a regularized curve.
    """
    curve_type = regularized_curve['type']
    params = regularized_curve['params']

    if curve_type == 'line':
        return {'reflection': True, 'rotation': 2}
    elif curve_type == 'circle':
        return {'reflection': True, 'rotation': float('inf')}
    elif curve_type == 'ellipse':
        xc, yc, a, b, theta = params
        if np.isclose(a, b):
            return {'reflection': True, 'rotation': float('inf')}
        else:
            return {'reflection': True, 'rotation': 2}
    elif curve_type == 'rectangle':
        cx, cy, width, height, angle = params
        if np.isclose(width, height):
            return {'reflection': True, 'rotation': 4}
        else:
            return {'reflection': True, 'rotation': 2}
    elif curve_type == 'unknown':
        # For unknown curves, we need to analyze the points
        points = regularized_curve.get('points')
        if points is not None:
            points = np.array(points)
            reflection_symmetry = find_reflection_symmetry(points)
            rotational_symmetry = find_rotational_symmetry(points)
            return {
                'reflection': reflection_symmetry is not None,
                'rotation': rotational_symmetry
            }
        else:
            return {'reflection': False, 'rotation': 1}
    else:
        return {'reflection': False, 'rotation': 1}

def process_symmetry(regularized_paths):
    """
    Process symmetry for all regularized paths.
    """
    symmetry_results = []
    for path in regularized_paths:
        path_symmetry = []
        for curve in path:
            symmetry = detect_symmetry(curve)
            path_symmetry.append(symmetry)
        symmetry_results.append(path_symmetry)
    return symmetry_results