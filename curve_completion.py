# File: curve_completion.py

import numpy as np
from scipy import interpolate
from curve_regularization import is_circle, fit_circle, is_ellipse, fit_ellipse

def complete_circle(partial_points):
    """
    Complete a partially occluded circle.
    """
    if len(partial_points) < 3:
        return None  # Not enough points to determine a circle

    center, radius = fit_circle(partial_points)
    
    # Generate points to complete the circle
    theta = np.linspace(0, 2*np.pi, 100)
    completed_points = np.array([
        center[0] + radius * np.cos(theta),
        center[1] + radius * np.sin(theta)
    ]).T
    
    return completed_points

def complete_ellipse(partial_points):
    """
    Complete a partially occluded ellipse.
    """
    if len(partial_points) < 5:
        return None  # Not enough points to determine an ellipse

    center, axes, angle = fit_ellipse(partial_points)
    
    # Generate points to complete the ellipse
    theta = np.linspace(0, 2*np.pi, 100)
    a, b = axes
    rotation = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])
    
    ellipse_points = np.dot(
        np.array([a * np.cos(theta), b * np.sin(theta)]).T,
        rotation.T
    )
    completed_points = ellipse_points + center
    
    return completed_points

def complete_curve_spline(partial_points, num_points=100):
    """
    Complete a partially occluded curve using spline interpolation.
    """
    if len(partial_points) < 2:
        return None  # Not enough points for interpolation

    # Parameterize the curve
    t = np.linspace(0, 1, len(partial_points))
    
    # Fit a spline to the partial points
    tck, u = interpolate.splprep([partial_points[:, 0], partial_points[:, 1]], s=0)
    
    # Generate more points along the spline
    new_points = interpolate.splev(np.linspace(0, 1, num_points), tck)
    
    return np.column_stack(new_points)

def complete_curve(partial_points):
    """
    Complete a partially occluded curve based on its detected shape.
    If completion is not possible, return the original points.
    """
    if is_circle(partial_points):
        completed = complete_circle(partial_points)
    elif is_ellipse(partial_points):
        completed = complete_ellipse(partial_points)
    else:
        completed = complete_curve_spline(partial_points)
    
    return completed if completed is not None else partial_points

def process_occlusions(regularized_paths):
    """
    Process occlusions for all regularized paths.
    """
    completed_paths = []
    for path in regularized_paths:
        completed_path = []
        for curve in path:
            if curve['type'] == 'unknown':
                completed_curve = complete_curve(curve['points'])
                completed_path.append({
                    'type': 'completed' if np.any(completed_curve != curve['points']) else 'unknown',
                    'original': curve,
                    'completed_points': completed_curve
                })
            else:
                completed_path.append(curve)
        completed_paths.append(completed_path)
    return completed_paths
    """
    Process occlusions for all regularized paths.
    """
    completed_paths = []
    for path in regularized_paths:
        completed_path = []
        for curve in path:
            if curve['type'] == 'unknown':
                completed_curve = complete_curve(curve['points'])
                completed_path.append({
                    'type': 'completed',
                    'original': curve,
                    'completed_points': completed_curve
                })
            else:
                completed_path.append(curve)
        completed_paths.append(completed_path)
    return completed_paths