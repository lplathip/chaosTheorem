from itertools import combinations
import math
from circleAndCircle import trace_circle_intersection
from circleAndPolygon import trace_polygon_circle_intersection

def calculate_distance(point1, point2):
    """Calculates the Euclidean distance between two points."""
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_distances(current_policy, preferences, grouppedNumbers):
    """Calculates the distances between the preferences and the current policy."""
    distances = []
    n = len(preferences)

    # Generate combinations of individual preferences
    for comb in combinations(range(n), grouppedNumbers):
        combination_name = ''.join(['P{}'.format(i+1) for i in comb])
        combination = [combination_name]
        for i in comb:
            combination.append(['P{}'.format(i+1), tuple(preferences[i]), calculate_distance(preferences[i], current_policy)])
        distances.append(combination)

    return distances

# Fixed preferences
preferences = [[10, 59], [60, 71], [25, 35], [48, 89], [75, 20]]
current_policy = [40, 35]
grouppedNumbers = 3

distances = calculate_distances(current_policy, preferences, grouppedNumbers)

#print current policy



# Making sure distance is working properly

for data in distances:
    print(data)

print("##################################")

#creating a winset

def generateWinset(combinationsList):

    returnList = []

    for items in combinationsList:


        itemList = [items[0]] # holding an array of items in the combination list to be stored in returnList

        c1Cords = items[1][1]
        c1Radius = items[1][2]

        c2Cords = items[2][1]
        c2Radius = items[2][2]

        intersectionPolygon = trace_circle_intersection(c1Cords,c1Radius,c2Cords,c2Radius)

        loopLength = len(items)-2 #each items list is in a form like this ['P1P2P3P4', ['P1', (10, 59), 38.41874542459709], ['P2', (60, 71), 41.182520563948], ['P3', (25, 35), 15.0], ['P4', (48, 89), 54.589376255824725]] so there are those amount of number of loops to go through after the first 2 circles

        for increment in range (1,loopLength):

            pos = 2+increment

            intersectionPolygon = trace_polygon_circle_intersection(intersectionPolygon,items[pos][1],items[pos][2])

        
        itemList.append(intersectionPolygon)
        returnList.append(itemList)



    return returnList

winSet = generateWinset(distances)

for data in winSet:
    print(data[0])
    print(data[1])
    print("-------------------")
