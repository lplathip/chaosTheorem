from shapely.geometry import Point
from shapely.ops import unary_union

def trace_circle_intersection(circle1_center, circle1_radius, circle2_center, circle2_radius):
    # Create the two circle objects
    circle1 = Point(circle1_center).buffer(circle1_radius)
    circle2 = Point(circle2_center).buffer(circle2_radius)

    # Find the intersection between the circles
    intersection = circle1.intersection(circle2)

    if intersection.is_empty:
        print("No intersection region") # This is theoretically not possible to happen as all points joins together at current policy, however, just in case there are errors
        return []

    # Check if the intersection has an actual area
    if intersection.area == 0.0:
        print("No intersection area")
        return []

    # Check if the intersection is a polygon (not a collection of polygons)
    if intersection.geom_type == 'Polygon':
        intersection_region = intersection
    else:
        # If the intersection is a collection of polygons, find their union
        intersection_region = unary_union(intersection)

    return intersection_region

