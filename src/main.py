import klayout.db as db
import math
import numpy as np
from DeviceLibrary import *

#this is a test branch
canvas = db.Layout()

# Define a new layer (Layer number: 1, Datatype: 0)
layer = canvas.layer(1, 0)

# Create a top cell
top_cell = canvas.create_cell("TOP")
waveguide_width = 0.45# Waveguide width in microns
radius = 100 # Radius of the bends in microns
straight_length = 10.0  # Length of the straight section in microns
gap = 0.2 # gap between bus waveguide and the straigt coupling waveguide in microns

arc_length=100


# Create the racetrack resonator
all_pass_ring_1= all_pass_ring(
                canvas=canvas,
                layer=layer,
                waveguide_width=waveguide_width,
                radius=radius,
                straight_length=straight_length,
                gap=gap
            )

all_pass_euler_ring_1= all_pass_euler_ring(
                canvas=canvas,
                layer=layer,
                waveguide_width=waveguide_width,
                arc_length=arc_length,
                straight_length=straight_length,
                gap=gap
            )

# Insert the racetrack resonator into the top cell
top_cell.insert(db.DCellInstArray(all_pass_ring_1.cell_index(), db.DTrans()))
offset = db.DVector(200, 0)
top_cell.insert(db.DCellInstArray(all_pass_euler_ring_1.cell_index(), db.DTrans(offset)))

# Write the layout to a GDS file
canvas.write("output/AllPassRing.gds")