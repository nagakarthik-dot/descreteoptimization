#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
from ortools.linear_solver import pywraplp

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solver(facilities, customers):
    
    no_f = len(facilities)
    no_c = len(customers)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    time_limit = 1800
    if no_f >= 500:
        time_limit *= 3
    solver.SetTimeLimit(int(time_limit * 1000))
    open = {}
    x    = {}
    for i in range(no_f):
        open[i] = solver.BoolVar(f'is facility {i} open')
        for j in range(no_c):
            x[i,j] = solver.BoolVar(f'does facility {i} serve customer {j}')
    for i in range(no_c):
        tempsum = 0
        tempsum += solver.Sum(x[j,i] for j in range(no_f))
        solver.Add(tempsum == 1)
    for i in range(no_f):
        sumOfDemands = 0
        sumOfDemands += solver.Sum(customers[j].demand * x[i,j] for j in range(no_c))
        solver.Add(sumOfDemands <= facilities[i].capacity)

    for i in range(no_f):
        sumrow = 0
        for j in range(no_c):
            sumrow += x[i,j]
        solver.Add(sumrow <= no_c * open[i])
    sumSetup = 0
    for i in range(no_f):
        sumSetup += open[i] * facilities[i].setup_cost 
    
    sumDist = 0
    for i in range(no_f):
        for j in range(no_c):
                sumDist += length(facilities[i].location, customers[j].location) * x[i,j]

    solver.Minimize(sumDist + sumSetup)
    solver.Solve()
    
    res = [-1]*no_c
    for i in range(no_f):
        for j in range(no_c): 
            if x[i,j].solution_value() == 1 :
                res[j] = i
    return res



def solve_it(input_data):

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))
    
    if len(facilities) >= 3000:             
        # trivial solution - pack the facilities one by one until all the customers are served
        solution = [-1]*len(customers)
        capacity_remaining = [f.capacity for f in facilities]

        facility_index = 0
        for customer in customers:
            
            if capacity_remaining[facility_index] >= customer.demand:
                solution[customer.index] = facility_index
                capacity_remaining[facility_index] -= customer.demand
                
            else:
                facility_index += 1
                assert capacity_remaining[facility_index] >= customer.demand
                solution[customer.index] = facility_index
                capacity_remaining[facility_index] -= customer.demand
                
    else:   
        solution = solver(facilities, customers)

    used = [0]*len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    # calculate the cost of the solution
    obj = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')