import klayout.db as db
import math
import numpy as np
from .BasicCurve import *
from .BasicComponents import *
from .Resonator import *


def grating_nature_lidar(
    canvas: db.Layout,
    layer: int,
    waveguide_width: float = 0.45,
    num_arcs: int = 2,
    initial_radius: float = 1.0,
    arc_spacing: float = 1.0
) -> db.Cell:
    
    # Create a new cell for the grating nature structure
    top_cell = canvas.create_cell("GRATING_NATURE")

    # Create the port waveguide 
    port_length = 1
    port_waveguide = straight_wg(
        canvas=canvas,
        layer=layer,
        length=port_length,
        width=waveguide_width
    )
    
    # Insert port waveguide into the top cell
    top_cell.insert(db.DCellInstArray(port_waveguide.cell_index(), db.DTrans(db.DTrans.R0, db.DVector(0, 0))))

    # Create and insert multiple arcs based on input parameters
    for i in range(num_arcs):
        # Calculate radius for each arc based on initial_radius and arc_spacing
        arc_radius = initial_radius + i * arc_spacing
        
        # Create an arc
        arc = arbitrary_circle_arc(
            center_x=0.0,
            center_y=0.0,
            radius=arc_radius,
            num_points=360,
            angle1=-45,
            angle2=45,

        )
        
        # Create a waveguide bend for each arc
        bend_wg_1 = bend_wg(
            canvas=canvas,
            layer=layer,
            curve_points=arc,
            width=0.5
        )

        # Insert each bend waveguide into the top cell with increasing offset in y direction
        top_cell.insert(db.DCellInstArray(bend_wg_1.cell_index(), db.DTrans(db.DVector(0, 0))))
    
    return top_cell