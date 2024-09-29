import numpy as np
from scipy.special import fresnel


def circle(
        center_x: float=0.0,
        center_y: float=0.0,
        radius: float=1,
        num_points: int = 360,
        angle:float=180,
) -> list[tuple[float, float]]:
    """Generate coordinates of points on the circumference of a circle.

    The function returns a list of (x, y) coordinates, which can be used to
    create `db.DPoint(x, y)` objects for each point on the circle's
    circumference.

    Args:
        center_x: X-coordinate of the circle's center.
        center_y: Y-coordinate of the circle's center.
        radius: Radius of the circle.
        num_points: Number of points to generate on the circle's circumference.
            Higher values produce a more fine-grained circle.

    Returns:
        A list of tuples containing (x, y) coordinates for points on the
        circle's circumference. These can be used directly for `db.DPoint(x, y)`.

    Example:
        .. code::

            points = BasicCurve.circle(center_x=0.0,center_y=0.0,radius=1,num_points= 360,angle=180,)
            for x, y in points:
                points.append(db.DPoint(x, y))

    """
    # Generate angles and precompute cos/sin values
    angles = np.linspace(0, np.pi*angle/180, num_points)

    # Calculate x and y coordinates
    x_coords = center_x + radius * np.cos(angles)
    y_coords = center_y + radius * np.sin(angles)

    # Return a list of tuples containing (x, y) coordinates
    return list(zip(x_coords, y_coords))

def arbitrary_circle_arc_1(
    p1: list[float],
    p2: list[float],
    radius: float,
    num_points: int = 100
) -> list[tuple[float, float]]:
    """Generate coordinates of points on an arc between two points.

    The function returns a list of (x, y) coordinates that define an arc
    passing through two points with a given radius.

    Args:
        p1: Coordinates of the first point [x1, y1].
        p2: Coordinates of the second point [x2, y2].
        radius: Radius of the circle that defines the arc.
        num_points: Number of points to generate on the arc. Higher values
            result in a more fine-grained arc.

    Returns:
        A list of tuples containing (x, y) coordinates for points along the arc.

    Raises:
        ValueError: If the radius is too small to form an arc between the points.

    Example:
        .. code::

            points = arc_points(p1=[1, 1], p2=[4, 2], radius=3, num_points=50)
            for x, y in points:
                print(f"Point: ({x}, {y})")

    """
    # Convert points to numpy arrays for easy calculations
    p1 = np.array(p1)
    p2 = np.array(p2)

    # Midpoint between p1 and p2
    midpoint = (p1 + p2) / 2

    # Distance between the two points
    distance = np.linalg.norm(p2 - p1)

    if distance > 2 * radius:
        raise ValueError("The radius is too small to form an arc between the points.")

    # Distance from the midpoint to the center of the circle
    h = np.sqrt(radius**2 - (distance / 2)**2)

    # Vector perpendicular to the line between p1 and p2
    direction = np.array([-(p2 - p1)[1], (p2 - p1)[0]])
    direction = direction / np.linalg.norm(direction)  # Normalize

    # Calculate the two possible centers of the circle
    center1 = midpoint + h * direction
    center2 = midpoint - h * direction

    # Select one of the centers (here we choose center1)
    center = center2

    # Angles for p1 and p2 relative to the center
    angle1 = np.arctan2(p1[1] - center[1], p1[0] - center[0])
    angle2 = np.arctan2(p2[1] - center[1], p2[0] - center[0])

    # Ensure angles are in the correct direction
    if angle2 < angle1:
        angle1, angle2 = angle2, angle1

    # Generate points on the arc
    angles = np.linspace(angle1, angle2, num_points)
    arc_points_x = center[0] + radius * np.cos(angles)
    arc_points_y = center[1] + radius * np.sin(angles)

    # Return a list of tuples containing (x, y) coordinates
    return list(zip(arc_points_x, arc_points_y))

def arbitrary_circle_arc_2(
        center_x: float=0.0,
        center_y: float=0.0,
        radius: float=1,
        num_points: int = 360,
        angle1:float=180,
        angle2:float=180,
) -> list[tuple[float, float]]:
    """Generate coordinates of points on the circumference of a circle.

    The function returns a list of (x, y) coordinates, which can be used to
    create `db.DPoint(x, y)` objects for each point on the circle's
    circumference.

    Args:
        center_x: X-coordinate of the circle's center.
        center_y: Y-coordinate of the circle's center.
        radius: Radius of the circle.
        num_points: Number of points to generate on the circle's circumference.
            Higher values produce a more fine-grained circle.

    Returns:
        A list of tuples containing (x, y) coordinates for points on the
        circle's circumference. These can be used directly for `db.DPoint(x, y)`.

    Example:
        .. code::

            points = BasicCurve.circle(center_x=0.0,center_y=0.0,radius=1,num_points= 360,angle=180,)
            for x, y in points:
                points.append(db.DPoint(x, y))

    """
    # Generate angles and precompute cos/sin values
    angles = np.linspace(np.pi*angle1/180, np.pi*angle2/180, num_points)

    # Calculate x and y coordinates
    x_coords = center_x + radius * np.cos(angles)
    y_coords = center_y + radius * np.sin(angles)

    # Return a list of tuples containing (x, y) coordinates
    return list(zip(x_coords, y_coords))

def euler_spiral(
        s: float,
        alpha: float,
        num_points: int = 1000,
        x_bias: float=0.0,
        y_bias: float=0.0,
) -> list[tuple[float, float]]:
    """
    Generate the coordinates of an Euler spiral for a given alpha value.

    Args:
        s: Arc length to generate the spiral.
        alpha: The alpha value controlling the curvature.
        num_points: The number of points to generate for the spiral (default is 1000).
        x_bias: the shift of the curve along the x axis,
        y_bias: the shift of the curve along the y axis,

    Returns:
        A list of tuples containing (x, y) coordinates for points on the
        Euler spiral.

    Example:
        .. code::

            points = euler_spiral(s=10.0, alpha=0.1, num_points=1000)
            for x, y in points:
                points.append(db.DPoint(x, y))
    """
    L = np.sqrt(np.pi / alpha)  # Constant ℓ
    s_vals = np.linspace(0, s, num_points)  # Arc length values

    # Compute Fresnel integrals
    fresnel_sin, fresnel_cos = fresnel(s_vals / L)

    # X and Y coordinates
    x_coords = L * fresnel_cos+x_bias # C(s/ℓ)
    y_coords = L * fresnel_sin+y_bias  # S(s/ℓ)

    # Return a list of tuples containing (x, y) coordinates
    return list(zip(x_coords, y_coords))

def euler_arc180_curve(
        s: float,
        alpha: float,
        num_points: int = 2000,
        x_bias: float = 0.0,
        y_bias: float = 0.0,
) -> list[tuple[float, float]]:
    """
    Generate the coordinates of a 180-degree Euler arc curve.

    Args:
        s: Arc length to generate the curve.
        alpha: The alpha value controlling the curvature.
        num_points: The number of points to generate for the curve (default is 2000).
        x_bias: The shift of the curve along the x-axis.
        y_bias: The shift of the curve along the y-axis.

    Returns:
        A list of tuples containing (x, y) coordinates for points on the 
        Euler arc curve.

    Example:
        .. code::

            points = euler_arc180_curve(s=10.0, alpha=0.1, num_points=2000)
            for x, y in points:
                points.append(db.DPoint(x, y))
    """
    bottom_curve_points = np.array(euler_spiral(s=s, alpha=alpha, num_points=num_points))
    
    # Calculate y-shift for reflecting
    y_shift = 2 * bottom_curve_points[-1, 1]
    
    # Reflect the bottom curve for the top arc
    top_curve_points = bottom_curve_points * [1, -1]
    top_curve_points[:, 1] += y_shift

    # Combine top and bottom curves
    curve_points = np.vstack((bottom_curve_points, top_curve_points[::-1]))
    
    # Smoothing transition by adding close points
    curve_points = np.insert(curve_points, 1, [curve_points[0, 0] + 0.001, curve_points[0, 1]], axis=0)
    curve_points = np.insert(curve_points, -1, [curve_points[-1, 0] + 0.001, curve_points[-1, 1]], axis=0)

    # Apply biases
    curve_points[:, 0] += x_bias
    curve_points[:, 1] += y_bias

    # Return a list of tuples containing (x, y) coordinates
    return list(map(tuple, curve_points))