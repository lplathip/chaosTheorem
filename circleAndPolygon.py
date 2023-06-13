from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

def trace_polygon_circle_intersection(polygon_coords, circle_center, circle_radius):
    # Create a polygon object from the given coordinates
    polygon = Polygon(polygon_coords)

    if polygon.is_empty:  # Check if the polygon is empty
        polygon = Point(0, 0)  # Replace with a Point object at (0, 0)

    # Create a circle object from the given center and radius
    circle = Point(circle_center).buffer(circle_radius)

    # Find the intersection between the polygon and the circle
    intersection = polygon.intersection(circle)

    if intersection.is_empty:  # Check if the intersection is empty, (again, theoretically shouldnt happen)
        return []
    elif intersection.geom_type == 'Point':  # Check if the intersection is a single point
        return [(intersection.x, intersection.y)]
    else:
        # If the intersection is a collection of polygons, find their union
        intersection_region = unary_union(intersection)

        if intersection_region.geom_type == 'Polygon':
            # Convert the polygon into a list of coordinate tuples so instead of returning in the format of ((39,28),(59,64),..) into [(39,28),(59,64),..] so it can be reused
            intersection_region = [coord for coord in intersection_region.exterior.coords]

    return intersection_region


