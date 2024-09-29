import klayout.db as db
import numpy as np
from DeviceLibrary import *

# Create a new layout
canvas = db.Layout()

# Create a top cell
top_cell = canvas.create_cell("TOP")

# Define the layer (you can choose any layer number and datatype)
layer_full_etch = canvas.layer(10, 2)
layer_partial_etch = canvas.layer(11, 4)



# Parameters for the rectangles
start_x = 0  # Starting x coordinate
start_y = 0  # Starting y coordinate
width1 = 0.33 # Width of the first rectangle
height1 = 0.45  # Height of the first rectangle
width2 = 0.33  # Width of the second rectangle
height2 = 0.8  # Height of the second rectangle
num_pairs = 20  # Number of rectangle pairs to generate

grating_ansys=grating_ansys_lidar(
    canvas=canvas,
    layer_full_etch=layer_full_etch,
    layer_partial_etch=layer_partial_etch,
    width1= 0.33,
    width2 = 0.33,
    height1 = 0.45,
    height2 = 0.8,
    num_pairs = 20,
)



# Create the output layout file
canvas.write("src/output/GratingAnsys1.gds")

print("GDS file generated: centered_connected_rectangles.gds")
