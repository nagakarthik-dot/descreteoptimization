#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import exchange_customers_between_vehicles as sol1
import Clarke_Wright_Algorithm as sol2
import numpy as np
import random


Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])
  


def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def opt2(vehicletours, customers):
    """ a two opt function that optimizes the provided vehicle tours 
    by swapping two customers generated randomly in a particular tour
    and accepts the solution if the tour cost of generated tour is 
    less than original cost """ 

    # specify depot as the first customer
    depot = customers[0]
    
    for vehicle_tour in vehicletours:
        tour_length = len(vehicle_tour)
        if tour_length>=2:
            
            # find the cost of current tour
            currCost = 0
            currCost += length(depot, customers[vehicle_tour[0]])
            for i in range(tour_length-1):
                currCost += length(customers[vehicle_tour[i]],customers[vehicle_tour[i+1]])
            currCost += length(customers[vehicle_tour[-1]], depot)

            # randomly generate two customers for specified number of iterations
            for _ in range(10000):
                newCost = 0
                n1 = random.randint(0,tour_length-1)
                n2 = random.randint(0,tour_length-1)

                # swap the two customers
                vehicle_tour[n1], vehicle_tour[n2] = vehicle_tour[n2], vehicle_tour[n1]

                # calculate new cost of tour after swapping
                newCost += length(depot, customers[vehicle_tour[0]])
                for i in range(tour_length-1):
                    newCost += length(customers[vehicle_tour[i]],customers[vehicle_tour[i+1]])
                newCost += length(customers[vehicle_tour[-1]], depot)

                # if the new cost is greater, swap the customers back, otherwise no change
                if newCost >= currCost:
                    vehicle_tour[n1], vehicle_tour[n2] = vehicle_tour[n2], vehicle_tour[n1]
   
    return vehicletours

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    
    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    #the depot is always the first customer in the input
    depot = customers[0] 

    #### SOLUTION STARTS HERE ####

    if customer_count == 16 or customer_count == 26 or customer_count == 200:  
        # a solution with 2-opt optimization that exchanges customers between different random vehicles if capacity constraint is not violated      
        vehicle_tours = sol1.myfun(customers, customer_count, vehicle_count, vehicle_capacity)     
    else:
        # use clarke wright algorithm
        vehicle_tours = sol2.myfun(customers, customer_count, vehicle_count, vehicle_capacity)      
        

    # optimizing the obtained solution using 2-opt
    vehicle_tours = opt2(vehicle_tours, customers)
    

    # calculate the cost of the solution; for each vehicle the length of the route
    obj = 0
    for v in range(vehicle_count):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            obj += length(depot,customers[vehicle_tour[0]])
            for i in range(0, len(vehicle_tour)-1):
                obj += length(customers[vehicle_tour[i]],customers[vehicle_tour[i+1]])
            obj += length(customers[vehicle_tour[-1]],depot)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(1) + '\n'
    for v in range(0, vehicle_count):
        outputData += str(depot.index) + ' ' + ' '.join([str(customers[customer].index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'

    file_path = f"Outputs\\output_{customer_count}_{vehicle_count}.txt" 
    with open(file_path, "w") as file:
        file.write(outputData)


    return outputData


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

