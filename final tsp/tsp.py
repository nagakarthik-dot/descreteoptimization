#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import itertools
from collections import namedtuple
from itertools import combinations
import time

Point = namedtuple("Point", ['x', 'y'])

CMP_THRESHOLD = 10 ** -6

def edge_length(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def point_dist(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def cycle_length(cycle, points):
    return sum(edge_length(points[cycle[i - 1]], points[cycle[i]]) for i in range(len(cycle)))

def is_valid_soln(cycle, points):
    return len(set(cycle[:-1])) == len(points) == len(cycle[:-1])

def greedy(points):
    cycle = [0]
    candidates = set(range(1, len(points)))
    while candidates:
        curr_point = cycle[-1]
        nearest_neighbor = min(candidates, key=lambda x: edge_length(points[curr_point], points[x]))
        cycle.append(nearest_neighbor)
        candidates.remove(nearest_neighbor)
    cycle.append(0)
    return cycle

def swap(cycle, points, start, end):
    new_cycle = cycle[:start] + cycle[start:end + 1][::-1] + cycle[end + 1:]
    new_obj = cycle_length(new_cycle, points)
    if new_obj < cycle_length(cycle, points) - CMP_THRESHOLD:
        return new_cycle, new_obj, True
    return cycle, cycle_length(cycle, points), False

def two_opt_solver(points, time_limit):
    cycle = list(range(len(points))) + [0]
    obj = cycle_length(cycle, points)
    improved = True
    start_time = time.time()

    while improved:
        if time.time() - start_time < time_limit:
        improved = False
        for start, end in combinations(range(1, len(cycle) - 1), 2):
            cycle, obj, swap_improved = swap(cycle, points, start, end)
            if swap_improved:
                improved = True
                break

    return cycle, obj

def solve_it(input_data):
    lines = input_data.split('\n')
    point_count = int(lines[0])
    points = [Point(float(parts[0]), float(parts[1])) for parts in (line.split() for line in lines[1:point_count+1])]
    
    cycle, obj = two_opt_solver(points,1800)
    ##obj,temp,cycle=k_opt(points,3,None)

    output_str = "{:.2f} 0\n".format(obj)
    output_str += ' '.join(map(str, cycle[:-1]))
    return output_str

def k_swap(cycle, length, endpoints, points):
    k = len(endpoints) 
    segments = [cycle[endpoints[i]:endpoints[i + 1]] for i in range(len(endpoints) - 1)]
    best_cycle = cycle
    best_length = length
    for num_reversed in range(k):
        for reversed_parts in itertools.combinations(segments,num_reversed):
            new_segments = []
            for i, segment in enumerate(segments):
                if i in reversed_parts:
                    new_segments.append(segment[::-1])
                else:
                    new_segments.append(segment)
            for i, permuted_segments in enumerate(itertools.permutations(new_segments)):
                if num_reversed == 0 and i == 0:
                    continue
                new_cycle = cycle[:endpoints[0]] + \
                    list(itertools.chain.from_iterable(permuted_segments)) + \
                    cycle[endpoints[-1] + 1:]
                new_length = cycle_length(new_cycle, points)
                if new_length < best_length:
                    best_cycle = new_cycle
                    best_length = best_length
    return best_cycle, best_length


def k_swap_iteration(cycle, points, k):
    point_count = len(points)
    length = cycle_length(cycle, points)
    improved = False
    for endpoints in itertools.combinations(range(1, point_count), k):
        new_cycle, new_length = k_swap(cycle, length, endpoints, points)
        # new_cycle, new_length = two_swap(cycle, length, endpoints[0], endpoints[1], points)
        if new_length < length:
            cycle = new_cycle
            length = new_length
            improved = True
            break
    return cycle, length, improved


def k_opt(points, k_max, initial):
    if initial:
        cycle = initial
    else:
        cycle = greedy(points)
    
    for k in range(2, k_max + 1):
        improved = True
        while improved:
            
            cycle, length, improved = k_swap_iteration(cycle, points, k)
    return cycle_length(cycle, points), 0, cycle

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file. Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
