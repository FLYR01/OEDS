import klayout.db as db
import numpy as np
from DeviceLibrary import *

canvas = db.Layout()
layer=canvas.layer(1,0)

grating1=grating_nature_lidar(
    canvas=canvas,
    layer=layer,
    waveguide_width= 0.45,
    num_arcs = 5,
    initial_radius = 5,
    arc_spacing =1,   
)


# Write the layout to a GDS file
canvas.write("src/output/GratingNature.gds")
print("GDS file 'result.gds' written successfully.")