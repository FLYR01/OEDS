import klayout.db as db
import numpy as np
from DeviceLibrary import *

canvas = db.Layout()
layer_1=canvas.layer(10,2)
layer_2=canvas.layer(11,4)


grating1=grating_nature_lidar(
    canvas=canvas,
    layer_full_etch=layer_1,
    layer_partial_etch=layer_2,
    waveguide_width= 0.45,
    transition_1_y=1.5,
    transition_1_x=0.45,
    transition_1_radius=0.8,  
    num_grating_elements= 4,
    arc_radii = [1.25, 1.9, 2.55, 3.2] ,
    grating_element_cladding = 0.5,
    element_width = 0.2,
)

# Write the layout to a GDS file
canvas.write("src/output/GratingNature1.gds")
print("GDS file 'result.gds' written successfully.")