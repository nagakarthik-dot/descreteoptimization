#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import itertools
from collections import namedtuple
from itertools import combinations
from time import time

Point = namedtuple("Point", ['x', 'y'])

def edge_length(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def cycle_length(cycle, points):
    return sum(edge_length(points[cycle[i - 1]], points[cycle[i]]) for i in range(len(cycle)))

def point_dist(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def is_valid_soln(cycle, points):
    return len(set(cycle[:-1])) == len(points) == len(cycle[:-1])

def greedy(points):
    cycle = [0]
    candidates = set(range(1, len(points)))
    while candidates:
        curr_point = cycle[-1]
        nearest_neighbor = None
        nearest_dist = math.inf
        for neighbor in candidates:
            neighbor_dist = edge_length(points[curr_point], points[neighbor])
            if neighbor_dist < nearest_dist:
                nearest_neighbor = neighbor
                nearest_dist = neighbor_dist
        cycle.append(nearest_neighbor)
        candidates.remove(nearest_neighbor)
    cycle.append(0)
    return cycle, cycle_length(cycle, points)

def swap(cycle, start, end, points, obj, CMP_THRESHOLD):
    improved = False
    new_cycle = cycle[:start] + cycle[start:end + 1][::-1] + cycle[end + 1:]
    new_obj = obj - (edge_length(points[cycle[start - 1]], points[cycle[start]]) +
               edge_length(points[cycle[end]], points[cycle[(end + 1)]])) + (edge_length(points[new_cycle[start - 1]], points[new_cycle[start]]) +
               edge_length(points[new_cycle[end]], points[new_cycle[(end + 1)]]))
    if new_obj < obj - CMP_THRESHOLD:
        cycle = new_cycle
        obj = new_obj
        improved = True
    return improved, cycle, obj

def two_opt_solver(points, t_threshold):
    CMP_THRESHOLD = 10 ** -6
    cycle = list(range(len(points))) + [0]
    obj = cycle_length(cycle, points)

    improved = True
    t = time()
    while improved:
        if t_threshold and time() - t >= t_threshold:
            break
        improved = False
        for start, end in combinations(range(1, len(cycle) - 1), 2):
            improved, cycle, obj = swap(cycle, start, end, points, obj, CMP_THRESHOLD)
            if improved:
                break
    return cycle, obj

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    point_count = int(lines[0])

    points = []
    for i in range(1, point_count + 1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    
    if point_count<=1000:
        cycle, obj = two_opt_solver(points,1800)
    else:
        cycle,obj=two_opt_solver(points,None)
    output_data = "{:.2f} 0\n".format(obj)
    output_data += ' '.join(map(str, cycle[:-1]))

    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file. Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
