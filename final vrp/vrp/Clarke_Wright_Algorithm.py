import math 
import numpy as np


def length(customer1, customer2):
   ###Function to return euclidean distance between two points
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)


def find_route_containing_customer(routes, customer):

    ###Returns the route in which particular customer is located 
    for i, route in enumerate(routes):
        if customer in route:
            return i
        
    return None

def is_feasible_merge(routes, route_i, route_j, demands, vehicle_capacity):

    ###Return true if merging the customer in route does not exceed the capacity of vehicle in that route 
    total_demand = sum(demands[customer] for customer in routes[route_i]) + sum(demands[customer] for customer in routes[route_j])

    return total_demand <= vehicle_capacity

def two_opt(route, customers):
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
    total_distance = 0

    for i in range(len(route)):
        total_distance += length(customers[route[i]], customers[route[(i + 1) % len(route)]])

    return total_distance


import numpy as np

def myfun(customers, customer_count, vehicle_count, vehicle_capacity):
    #  Build the distance matrix (D)
    depot = customers[0]
    D = []  
    for i in range(customer_count):
        temp = []
        for j in range(customer_count):
            temp.append(length(customers[i], customers[j]))  
        D.append(temp)

    # Compute savings matrix using Clark and Wright Savings Algorithm
    demands = [customer.demand for customer in customers]  # Demand for each customer (excluding depot)
    savings = np.zeros((customer_count, customer_count))
    
    # Calculate savings for each pair of customers (i, j)
    for i in range(1, customer_count):  
        for j in range(i+1, customer_count):
            savings[i][j] = D[0][i] + D[0][j] - D[i][j]  
            savings[j][i] = savings[i][j]  

    # Sort pairs of customers by savings in descending order
    sorted_indices = np.argsort(-savings, axis=None) 
    sorted_i, sorted_j = np.unravel_index(sorted_indices, savings.shape)  
    
    # Initialize vehicle tours: start with each customer on a separate route
    vehicle_tours = [[i] for i in range(1, customer_count)]
    # Merge routes based on savings
    for k in range(len(sorted_i)):
        i, j = sorted_i[k], sorted_j[k]
        
        # Ensure valid customers (not depot, not the same customer)
        if i == 0 or j == 0 or i == j:
            continue
        
        # Find the routes that contain customer i and j
        route_i = find_route_containing_customer(vehicle_tours, i)
        route_j = find_route_containing_customer(vehicle_tours, j)
        # Check if merging the two routes is feasible
        if route_i != route_j and is_feasible_merge(vehicle_tours, route_i, route_j, demands, vehicle_capacity):
            # Merge route_j into route_i and remove route_j
            vehicle_tours[route_i] += vehicle_tours[route_j]
            del vehicle_tours[route_j]

    while len(vehicle_tours) < vehicle_count:
        vehicle_tours.append([])
    ### Optimize each route using the 2-OPT algorithm to minimize the distance traveled
    for v in range(vehicle_count):
        if len(vehicle_tours[v]) > 1:
            vehicle_tours[v].insert(0, 0) 
            vehicle_tours[v] = two_opt(vehicle_tours[v], customers)  
            vehicle_tours[v] = [i for i in vehicle_tours[v] if i != 0]

    return vehicle_tours