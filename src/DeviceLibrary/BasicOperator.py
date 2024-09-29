def find_middle_point(
        points: list[tuple[float, float]]
) -> tuple[float, float]:
    """Find the middle point in a list of (x, y) coordinates.

    The function returns the middle point from a list of coordinates. If the 
    list has an odd number of points, it returns the exact middle point. If 
    the list has an even number of points, it returns the average of the two 
    middle points.

    Args:
        points: A list of (x, y) tuples representing points.

    Returns:
        A tuple (x, y) representing the middle point.

    Example:
        .. code::

            middle_point = find_middle_point(arc_points)
            print(middle_point)

    """
    n = len(points)
    
    # Check if number of points is odd or even and calculate the middle point
    if n % 2 == 1:
        # Odd number of points, return the middle point
        middle_point = points[n // 2]
    else:
        # Even number of points, return the average of the two middle points
        point1 = points[n // 2 - 1]
        point2 = points[n // 2]
        middle_point = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

    return middle_point
