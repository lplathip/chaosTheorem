from itertools import combinations
import math
from circleAndCircle import trace_circle_intersection
from circleAndPolygon import trace_polygon_circle_intersection
from anytree import Node, RenderTree, findall
from collections import deque
from matplotlib.path import Path
import json
import webbrowser
import os
from matplotlib import pyplot as plt

def calculate_distance(point1, point2):
    """Calculates the Euclidean distance between two points."""
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def point_in_polygon(point,polygon): #to check if the endPolicy is in the winset
    path = Path(polygon)

    return path.contains_point(point)

def calculate_combinations(current_policy, preferences, grouppedNumbers):
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

def generateWinset(combinationsList,current_policy,endPoint):

    if current_policy != endPoint:

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

            #to create Choose alternatives successively further away from the “middle,” thereby creating larger and larger win sets.

            if len(intersectionPolygon) == 0:
                itemList.append(None)

            else:

                if point_in_polygon(endPoint, intersectionPolygon) == True:
                    itemList.append(endPoint)

                else:
                    temp = []
                    for data in intersectionPolygon:

                        temp.append(calculate_distance(data,current_policy))
                    maxDistance = max(temp)
                    itemList.append(intersectionPolygon[temp.index(maxDistance)])

            returnList.append(itemList)

        return returnList
    else:
        return []
    
def winSetToNewPolicy(winsetData):
    newPolicyCords = []

    for data in winsetData:
        if data[2] != None:
            newPolicyCords.append(data[2])

    return newPolicyCords

import csv

def export_tree_data(root_node):
    """Exports the tree data in CSV format compatible with Gephi."""
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory path of the main script
    file_path = os.path.join(script_dir, "tree_data.csv")  # Combine the directory path with the filename

    nodes = []
    edges = []

    node_id = 1
    node_id_mapping = {}

    # Traverse the tree and collect node and edge data
    for pre, fill, node in RenderTree(root_node):
        node_label = f'"{node.name}"'  # Enclose the label value in quotation marks
        nodes.append([node_id, node_label])
        node_id_mapping[str(node)] = node_id
        node_id += 1

        if node.parent:
            parent_id = node_id_mapping[str(node.parent)]
            edges.append([parent_id, node_id])

    # Save the node and edge data to a CSV file in the specified directory
    with open(file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Id", "Label"])
        writer.writerows(nodes)
        writer.writerow(["Source", "Target"])
        writer.writerows(edges)

    print(f"tree_data.csv created successfully in {file_path}")




def main():
    # Setting fixed conditions
    preferences = [[10, 59], [60, 71], [25, 35], [48, 89], [75, 20]]
    endPoint = (50, 50)
    groupedNumbers = 3

    root_node = Node((40, 35))  # the start current policy
    queue = deque([root_node])
    max_loops = 3
    loops = 0

    while queue and loops < max_loops:
        queue_length = len(queue)

        for _ in range(queue_length):
            current_node = queue.popleft()
            combinations = calculate_combinations(current_node.name, preferences, groupedNumbers)
            new_policy_list = winSetToNewPolicy(generateWinset(combinations, current_node.name, endPoint))

            for cords in new_policy_list:
                child_node = Node(cords, parent=current_node)
                queue.append(child_node)

        loops += 1

    # Print the tree
    for pre, fill, node in RenderTree(root_node):
        print(f"{pre}{node.name}")

    # Export the tree data to JSON
    export_tree_data(root_node)



if __name__ == "__main__":
    main()
    

