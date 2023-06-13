from shapely.geometry import Point
from shapely.ops import unary_union

def trace_circle_intersection(circle1_center, circle1_radius, circle2_center, circle2_radius):
    # Create the two circle objects
    circle1 = Point(circle1_center).buffer(circle1_radius)
    circle2 = Point(circle2_center).buffer(circle2_radius)

    # Find the intersection between the circles
    intersection = circle1.intersection(circle2)

    if intersection.is_empty:
        print("No intersection region")
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

# Circle coordinates and radius for P1
circle1_center = (10, 59)
circle1_radius = 38.41874542459709

# Circle coordinates and radius for P2
circle2_center = (60, 71)
circle2_radius = 41.182520563948

# Calculate the intersection region
intersection_region = trace_circle_intersection(circle1_center, circle1_radius, circle2_center, circle2_radius)

# Print the result
if intersection_region:
    print("Intersection Region:", list(intersection_region.exterior.coords)[:-1])
else:
    print("No intersection region")
