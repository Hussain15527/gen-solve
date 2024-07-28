# File: visualization.py

import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend which doesn't require additional dependencies
import matplotlib.pyplot as plt
import numpy as np
import os

import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend which doesn't require additional dependencies
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_curve(ax, curve, color='b', label=None):
    """Plot a single curve on the given axes."""
    try:
        print(f"Plotting curve of type: {curve['type']}")
        if curve['type'] == 'line':
            a, b, c = curve['params']
            x = np.linspace(min(curve['points'][:, 0]), max(curve['points'][:, 0]), 100)
            y = (-a*x - c) / b
            ax.plot(x, y, color, label=label)
        elif curve['type'] in ['circle', 'ellipse']:
            if curve['type'] == 'circle':
                center, radius = curve['params'][0:2], curve['params'][2]
                angle = np.linspace(0, 2*np.pi, 100)
                x = center[0] + radius * np.cos(angle)
                y = center[1] + radius * np.sin(angle)
            else:  # ellipse
                center, axes, angle = curve['params'][0:2], curve['params'][2:4], curve['params'][4]
                t = np.linspace(0, 2*np.pi, 100)
                a, b = axes
                x = center[0] + a*np.cos(t)*np.cos(angle) - b*np.sin(t)*np.sin(angle)
                y = center[1] + a*np.cos(t)*np.sin(angle) + b*np.sin(t)*np.cos(angle)
            ax.plot(x, y, color, label=label)
        elif curve['type'] == 'rectangle':
            center, (width, height), angle = curve['params'][0:2], curve['params'][2:4], curve['params'][4]
            rect = plt.Rectangle(center, width, height, angle=np.degrees(angle), 
                                 fill=False, color=color, label=label)
            ax.add_patch(rect)
        elif curve['type'] == 'completed':
            if 'completed_points' in curve and curve['completed_points'] is not None:
                ax.plot(curve['completed_points'][:, 0], curve['completed_points'][:, 1], color, label=label)
            else:
                print(f"Warning: No completed points for curve {label}")
        elif curve['type'] == 'unknown':
            if 'points' in curve and curve['points'] is not None:
                ax.plot(curve['points'][:, 0], curve['points'][:, 1], color, label=label)
            else:
                print(f"Warning: No points for unknown curve {label}")
        else:
            print(f"Warning: Unknown curve type '{curve['type']}' for curve {label}")
        print(f"Successfully plotted curve of type: {curve['type']}")
    except Exception as e:
        print(f"Error plotting curve of type {curve['type']}: {str(e)}")

def visualize_results(completed_paths, output_path):
    """Visualize the results of curve detection, regularization, and completion."""
    print(f"Starting visualization of results. Output path: {output_path}")
    try:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for i, path in enumerate(completed_paths):
            print(f"Processing path {i+1} of {len(completed_paths)}")
            for j, curve in enumerate(path):
                if curve['type'] == 'completed':
                    plot_curve(ax, curve, color='r', label=f'Completed (Path {i+1}, Curve {j+1})')
                    plot_curve(ax, curve['original'], color='b', label=f'Original (Path {i+1}, Curve {j+1})')
                else:
                    plot_curve(ax, curve, color='g', label=f'{curve["type"].capitalize()} (Path {i+1}, Curve {j+1})')

        ax.set_aspect('equal', 'box')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_title('Curve Detection, Regularization, and Completion Results')
        plt.tight_layout()
        print(f"Saving figure to {output_path}")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"Results visualization saved to {output_path}")
    except Exception as e:
        print(f"Error in visualize_results: {str(e)}")

def visualize_symmetry(completed_paths, symmetry_results, output_path):
    """Visualize the symmetry detection results."""
    print(f"Starting visualization of symmetry. Output path: {output_path}")
    try:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for i, (path, path_symmetry) in enumerate(zip(completed_paths, symmetry_results)):
            print(f"Processing path {i+1} of {len(completed_paths)}")
            for curve, symmetry in zip(path, path_symmetry):
                if symmetry['reflection']:
                    color = 'r'
                    label = 'Reflection Symmetry'
                elif symmetry['rotation'] > 1:
                    color = 'g'
                    label = f'Rotational Symmetry (Order {symmetry["rotation"]})'
                else:
                    color = 'b'
                    label = 'No Symmetry'
                
                plot_curve(ax, curve, color=color, label=label)

        ax.set_aspect('equal', 'box')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_title('Symmetry Detection Results')
        plt.tight_layout()
        print(f"Saving figure to {output_path}")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"Symmetry visualization saved to {output_path}")
    except Exception as e:
        print(f"Error in visualize_symmetry: {e}")

def check_matplotlib_backend():
    """Check and print the current Matplotlib backend."""
    print(f"Current Matplotlib backend: {matplotlib.get_backend()}")

# Test function to check if visualization is working
def test_visualization():
    print("Testing visualization...")
    check_matplotlib_backend()
    
    # Create a simple test plot
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4])
    ax.set_title('Test Plot')
    
    # Save the test plot
    test_output = 'test_plot.png'
    print(f"Attempting to save test plot to {test_output}")
    plt.savefig(test_output)
    plt.close(fig)
    
    if os.path.exists(test_output):
        print(f"Test plot saved successfully to {test_output}")
        print(f"File size: {os.path.getsize(test_output)} bytes")
    else:
        print("Failed to save test plot")

if __name__ == "__main__":
    test_visualization()