#!/usr/bin/env python3
"""
Convert all Jupyter notebooks in the current directory to HTML,
executing each to include its outputs, and place the results
into a newly created subfolder named "html".
"""
import subprocess
import sys
from pathlib import Path

def main():
    # Define base and output directories
    base_dir = Path.cwd()
    output_dir = base_dir / 'html'
    # Create output folder if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    # Find all .ipynb files directly in the current directory
    notebooks = list(base_dir.glob('*.ipynb'))
    if not notebooks:
        print("No notebooks found in the current directory.")
        return

    # Convert each notebook to HTML with outputs
    for nb in notebooks:
        print(f"Converting {nb.name}...")
        try:
            subprocess.run([
                sys.executable,
                '-m', 'nbconvert',
                '--to', 'html',
                '--execute',
                '--output-dir', str(output_dir),
                str(nb)
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {nb.name}: {e}")

    print("All notebooks have been converted and saved to the 'html' folder.")

if __name__ == '__main__':
    main()


