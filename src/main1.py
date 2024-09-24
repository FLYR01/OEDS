import klayout.db as db
import numpy as np
from DeviceLibrary import *


# Usage
def main():
    layout = db.Layout()
    layer=layout.layer(1,0)

    top_cell = adiabatic_euler_racetrack_resonator(layout,layer)
    all_pass_adiabatic_euler_ring_1 = all_pass_adiabatic_euler_ring(
            canvas=layout,
            layer=layer,
            waveguide_width=0.45,
            arc_length1 = 100.0,
            arc_length2 = 80.0,
            straight_length = 10.0,
            gap=0.2,
            )
    
    
    # Write the layout to a GDS file
    layout.write("C:/Users/32232/Documents/OEDS/OEDS/src/output/AllPassRing.gds")
    print("GDS file 'result.gds' written successfully.")

main()
