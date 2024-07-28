# Curvetopia Environment Setup Guide

This guide will walk you through setting up a virtual environment for the Curvetopia project using `venv`, which is included in Python 3.3 and later.

## Prerequisites

- Python 3.6 or later
- pip (usually comes with Python)

## Steps

1. **Clone the Curvetopia repository** (assuming it's on a platform like GitHub):

   ```
   git clone https://github.com/your-username/curvetopia.git
   cd curvetopia
   ```

2. **Create a virtual environment**:

   On macOS and Linux:
   ```
   python3 -m venv env
   ```

   On Windows:
   ```
   python -m venv env
   ```

3. **Activate the virtual environment**:

   On macOS and Linux:
   ```
   source env/bin/activate
   ```

   On Windows:
   ```
   .\env\Scripts\activate
   ```

   Your command prompt should now show `(env)` at the beginning, indicating that the virtual environment is active.

4. **Install the required packages**:

   ```
   pip install -r requirements.txt
   ```

5. **Verify the installation**:

   ```
   python -c "import numpy, scipy, cv2, skimage, matplotlib, svgwrite, cairosvg; print('All packages installed successfully!')"
   ```

   If you see the success message without any errors, your environment is set up correctly.

## Usage

- Always activate the virtual environment before working on the project:

  On macOS and Linux:
  ```
  source env/bin/activate
  ```

  On Windows:
  ```
  .\env\Scripts\activate
  ```

- To deactivate the virtual environment when you're done:

  ```
  deactivate
  ```

## Troubleshooting

- If you encounter any issues with OpenCV on macOS, you might need to install it using Homebrew:

  ```
  brew install opencv
  ```

- On some systems, you might need to use `python` instead of `python3` and `pip` instead of `pip3`. Adjust the commands accordingly.

- If you're having trouble with `cairosvg`, make sure you have Cairo installed on your system. On Ubuntu or Debian, you can install it with:

  ```
  sudo apt-get install libcairo2-dev
  ```

  On macOS with Homebrew:

  ```
  brew install cairo
  ```

Remember to keep your `requirements.txt` file updated if you add or remove any dependencies during development.