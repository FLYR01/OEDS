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

def euler_spiral(
        s: float,
        alpha: float,
        num_points: int = 1000
) -> list[tuple[float, float]]:
    """
    Generate the coordinates of an Euler spiral for a given alpha value.

    Args:
        s: Arc length to generate the spiral.
        alpha: The alpha value controlling the curvature.
        num_points: The number of points to generate for the spiral (default is 1000).

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
    x_coords = L * fresnel_cos  # C(s/ℓ)
    y_coords = L * fresnel_sin  # S(s/ℓ)

    # Return a list of tuples containing (x, y) coordinates
    return list(zip(x_coords, y_coords))
