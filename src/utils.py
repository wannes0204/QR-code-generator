"""
By: De Vleeschouwer Wannes
Email: wannes.devleeschouwer@student.uantwerpen.be

Created: 18/11/2025 (dd-mm-yyyy)
Last modification: 18/11/2025 (dd-mm-yyyy)

Description: General utility functions for the project.
"""

# Standard library modules
import os


# Define assets directory
try:
    # Gets project directory from the file path
    src_dir = os.path.dirname(__file__)
    project_dir = os.path.join(src_dir, "..")
except NameError:
    # If running from the interactive console, __file__ not defined
    project_dir = os.getcwd()
    
assets_dir = os.path.join(project_dir, "assets")
output_dir = os.path.join(assets_dir, "output")
input_dir = os.path.join(assets_dir, "input")
