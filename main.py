# File: main.py

import os
import numpy as np
from png_processor import png_to_polylines, save_polylines_to_csv, test_ximgproc
from curve_regularization import read_csv, process_paths
from symmetry_detection import process_symmetry
from curve_completion import process_occlusions
from visualization import visualize_results, visualize_symmetry, test_visualization

def process_image(png_path, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate base filename
    base_filename = os.path.splitext(os.path.basename(png_path))[0]

    print(f"Processing {png_path}...")

    # Process PNG to polylines
    try:
        polylines = png_to_polylines(png_path)
        print(f"Successfully extracted {len(polylines)} polylines from the image.")
    except Exception as e:
        print(f"Error during PNG to polyline conversion: {str(e)}")
        return

    # Save polylines to CSV
    csv_path = os.path.join(output_dir, f"{base_filename}_polylines.csv")
    try:
        save_polylines_to_csv(polylines, csv_path)
        print(f"Polylines saved to {csv_path}")
        print(f"CSV file size: {os.path.getsize(csv_path)} bytes")
        with open(csv_path, 'r') as f:
            print(f"First few lines of CSV:")
            for i, line in enumerate(f):
                if i < 5:  # Print first 5 lines
                    print(line.strip())
                else:
                    break
    except Exception as e:
        print(f"Error saving polylines to CSV: {str(e)}")
        return

    # Read CSV and regularize curves
    try:
        paths = read_csv(csv_path)
        print(f"Successfully read {len(paths)} paths from CSV.")
        regularized_paths = process_paths(paths)
        print(f"Successfully regularized {len(regularized_paths)} paths.")
        print("Regularized paths summary:")
        for i, path in enumerate(regularized_paths):
            print(f"  Path {i+1}: {len(path)} curves")
            for j, curve in enumerate(path):
                print(f"    Curve {j+1}: Type - {curve['type']}")
    except Exception as e:
        print(f"Error during curve regularization: {str(e)}")
        return

    # Detect symmetry in regularized paths
    try:
        symmetry_results = process_symmetry(regularized_paths)
        print("Symmetry detection completed.")
    except Exception as e:
        print(f"Error during symmetry detection: {str(e)}")
        symmetry_results = None

    # Complete occluded curves
    try:
        completed_paths = process_occlusions(regularized_paths)
        print("Curve completion process finished.")
        print("Completed paths summary:")
        for i, path in enumerate(completed_paths):
            print(f"  Path {i+1}: {len(path)} curves")
            for j, curve in enumerate(path):
                print(f"    Curve {j+1}: Type - {curve['type']}")
    except Exception as e:
        print(f"Error during curve completion: {str(e)}")
        completed_paths = regularized_paths  # Use regularized paths if completion fails

    # Visualize results
    try:
        print(f"Preparing to visualize results for {len(completed_paths)} paths")
        results_path = os.path.join(output_dir, f"{base_filename}_results.png")
        visualize_results(completed_paths, results_path)
        print(f"Checking if results visualization was saved: {os.path.exists(results_path)}")
        if symmetry_results:
            print(f"Preparing to visualize symmetry for {len(symmetry_results)} paths")
            symmetry_path = os.path.join(output_dir, f"{base_filename}_symmetry.png")
            visualize_symmetry(completed_paths, symmetry_results, symmetry_path)
            print(f"Checking if symmetry visualization was saved: {os.path.exists(symmetry_path)}")
        print(f"Visualizations should be saved to {output_dir}/{base_filename}_results.png and {base_filename}_symmetry.png")
    except Exception as e:
        print(f"An error occurred during visualization: {str(e)}")
        print("Continuing with text output...")

    # Print results
    print(f"\nProcessed {png_path}")
    print(f"Number of paths: {len(completed_paths)}")
    for i, path in enumerate(completed_paths):
        print(f"Path {i + 1}:")
        for j, curve in enumerate(path):
            print(f"  Curve {j + 1}:")
            if curve['type'] == 'completed':
                print(f"    Type: Completed (original: {curve['original']['type']})")
                if curve['completed_points'] is not None:
                    print(f"    Completed points: {len(curve['completed_points'])} points")
                else:
                    print("    Completion was not possible")
            else:
                print(f"    Type: {curve['type']}")
                if 'params' in curve:
                    print(f"    Params: {curve['params']}")
            if symmetry_results:
                symmetry = symmetry_results[i][j]
                if symmetry is not None:
                    print(f"    Symmetry: Reflection - {symmetry['reflection']}, Rotation - {symmetry['rotation']}")
                else:
                    print("    Symmetry: Could not be determined")

def main():
    # Test for ximgproc availability
    if not test_ximgproc():
        print("ximgproc is not available. The program may not function correctly.")
        return

    # Test visualization
    test_visualization()

    # Example usage
    png_path = "./png/simplify.png"  # Replace with your PNG file path
    output_dir = "output"
    
    try:
        process_image(png_path, output_dir)
    except Exception as e:
        print(f"An unexpected error occurred while processing the image: {str(e)}")

if __name__ == "__main__":
    main()