import klayout.db as db
import math
import numpy as np
from .BasicCurve import *
from .BasicComponents import *
from .Resonator import *
from .BasicOperator import *

def grating_nature_lidar(
    canvas: db.Layout,
    layer_full_etch: int,
    layer_partial_etch: int,
    waveguide_width: float = 0.45,
    transition_1_x: float = 1,
    transition_1_y: float = 2,
    transition_1_radius: float = 1.5,
    pitch: float = 0.78,
    element_width: float = 0.2,
    num_grating_elements: int = 4,
    arc_radii: list = [3, 6, 7, 7],
    grating_element_cladding: float = 0.45,
    
) -> db.Cell:
    """
    Create a grating structure and insert it into a layout.

    Args:
        canvas: The layout object where the structure will be added.
        layer_full_etch: The full etch layer where the structure should be inserted.
        layer_partial_etch: The partial etch layer (unused in this version).
        waveguide_width: The width of the port waveguide.
        transition_1_x: X size for the first transition structure.
        transition_1_y: Y-size for the first transition structure.
        transition_1_radius: Radius arc of size for the first transition structure.
        pitch: Spacing between the grating elements.
        element_width: The width of each grating element.
        num_grating_elements: Number of grating elements to insert.
        arc_radii: List of radii for each grating element's arc.

    Returns:
        A db.Cell object containing the grating structure.
    """
    
    # Helper function to create and insert arcs
    def create_arc(p1, p2, radius, num_points):
        return arbitrary_circle_arc_1(p1=p1, p2=p2, radius=radius, num_points=num_points)
    




    # Create a new cell for the grating structure
    top_cell = canvas.create_cell("GRATING_NATURE")

    # Create and insert the port waveguide
    port_length = 1.0
    port_waveguide = straight_wg(
        canvas=canvas,
        layer=layer_full_etch,
        length=port_length,
        width=waveguide_width,
    )
    top_cell.insert(db.DCellInstArray(port_waveguide.cell_index(), db.DTrans(db.DTrans.R0, db.DVector(0, 0))))

    # Calculate coordinates for the arc between two points
    p1 = [port_length * 1000 + transition_1_x * 1000, transition_1_y * 1000 / 2]
    p2 = [port_length * 1000 + transition_1_x * 1000, -transition_1_y * 1000 / 2]

    # Generate the initial transition curve points
    curve_points = create_arc(p1=p1, p2=p2, radius=transition_1_radius * 1000, num_points=1000)

    # Add port waveguide end points to the curve
    additional_p1 = [port_length * 1000, -waveguide_width * 1000 / 2]
    additional_p2 = [port_length * 1000, waveguide_width * 1000 / 2]
    middle_ponit_1=find_middle_point(curve_points)
    x_shift_1=middle_ponit_1[0]-curve_points[0][0]
    curve_points.insert(0, tuple(additional_p1))
    curve_points.append(tuple(additional_p2))
   

    # Create and insert the transition polygon
    transition_polygon = db.Polygon([db.Point(*pt) for pt in curve_points])
    top_cell.shapes(layer_full_etch).insert(transition_polygon)

    # Loop to create grating elements
    current_p1 = [p1[0], p1[1]+grating_element_cladding*1000]
    current_p2 = [p2[0], p2[1]-grating_element_cladding*1000]
    for i in range(num_grating_elements):
        arc_p1 = [current_p1[0], current_p1[1]]
        arc_p2 = [current_p2[0], current_p2[1]]
        radius = arc_radii[i] * 1000  # Get radius from the list

        # Create arc for the grating element
        arc_points = create_arc(p1=arc_p1, p2=arc_p2, radius=radius, num_points=100)
        # Add 1000 to the first element of each tuple in arc_points
        
        update_arc_points = [(x, y) for (x, y) in arc_points]
        middle_ponit=find_middle_point(update_arc_points)
        x_shift=middle_ponit[0]-update_arc_points[0][0]
        new_arc_points = [(x+pitch*1000*(i+1)-x_shift+x_shift_1, y) for (x, y) in update_arc_points]


        # Create and insert the grating element
        grating_element = db.Path(new_arc_points, width=element_width * 1000)
        top_cell.shapes(layer_full_etch).insert(grating_element)

        # Update current points for the next iteration
        current_p1 = arc_p1
        current_p2 = arc_p2

    return top_cell
