import math 
import numpy as np


def length(customer1, customer2):
    """ Function to return euclidean distance between two points """
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)


def find_route_containing_customer(routes, customer):

    """ Returns the route in which particular customer is located """
    for i, route in enumerate(routes):
        if customer in route:
            return i
        
    return None

def is_feasible_merge(routes, route_i, route_j, demands, vehicle_capacity):

    """ Return true if merging the customer in route does not exceed the capacity of vehicle in that route """
    total_demand = sum(demands[customer] for customer in routes[route_i]) + sum(demands[customer] for customer in routes[route_j])

    return total_demand <= vehicle_capacity

def two_opt(route, customers):
    """ Applies the 2-opt algorithm to improve the given route"""
    improved = True
    best_distance = calculate_route_distance(route, customers)
    
    while improved:
        improved = False
        for i in range(0, len(route) - 1):
            for j in range(i + 2, len(route)):
                new_route = route.copy()
                new_route[i:j+1] = reversed(route[i:j+1])  # Reverse the order of the nodes in the selected segment
                new_distance = calculate_route_distance(new_route, customers)
                
                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    improved = True

        route.insert(0, route[len(route)-1])
        route.pop()
    return route

def calculate_route_distance(route, customers):
    """Calculates the total distance of a route"""
    total_distance = 0

    for i in range(len(route)):
        total_distance += length(customers[route[i]], customers[route[(i + 1) % len(route)]])

    return total_distance


def myfun(customers, customer_count, vehicle_count, vehicle_capacity):

    # Distance matrix
    depot = customers[0]
    D = [] 
    for i in range(customer_count):
        temp = []
        for j in range(customer_count):
            temp.append(length(customers[i], customers[j]))
        D.append(temp)
    

    # Clark and Wright Saving method
    demands = [customer.demand for customer in customers]  # Demand of each customer (excluding depot)
    # Step 1: Calculate savings
    savings = np.zeros((customer_count, customer_count))
    for i in range(customer_count):
        for j in range(i+1, customer_count):
            savings[i][j] = D[depot.index][i] + D[depot.index][j] - D[i][j]
            savings[j][i] = savings[i][j]

    # Step 2: Sort pairs of customers in descending order of savings
    sorted_indices = np.argsort(-savings, axis=None)
    sorted_i, sorted_j = np.unravel_index(sorted_indices, savings.shape)
    s_i = []
    s_j = []
    k = 0
    while k < len(sorted_i):
        if sorted_i[k] != 0 and sorted_j[k] != 0 and sorted_i[k] != sorted_j[k]:
            s_i.append(sorted_i[k])
            s_j.append(sorted_j[k])
        k+=1
    vehicle_tours = [[i] for i in range(1, customer_count)]

    # Step 4: Merge routes based on savings
    for k in range(len(s_i)):
        i, j = s_i[k], s_j[k]
        route_i = find_route_containing_customer(vehicle_tours, i)
        route_j = find_route_containing_customer(vehicle_tours, j)

        if route_i != route_j and is_feasible_merge(vehicle_tours, route_i, route_j, demands, vehicle_capacity):
            vehicle_tours[route_i] += vehicle_tours[route_j]
            del vehicle_tours[route_j]
        
    cnt = 0
    if len(vehicle_tours) < vehicle_count:
        cnt = vehicle_count - len(vehicle_tours)
    for v in range(cnt):
        vehicle_tours.append([])

    # Apply 2-OPT
    for v in range(vehicle_count):
        if len(vehicle_tours[v]) > 1:
            vehicle_tours[v].insert(0, depot.index)
            vehicle_tours[v] = two_opt(vehicle_tours[v], customers)
            temp = vehicle_tours[v].copy()
            vehicle_tours[v] = []
            for i in temp:
                if i != 0:
                    vehicle_tours[v].append(i)
                else:
                    break
            for i in reversed(temp):
                if i != 0:
                    vehicle_tours[v] = [i] + vehicle_tours[v]
                else:
                    break

    return vehicle_tours
    