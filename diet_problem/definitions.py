# definitions.py
import os
from gurobipy import Model, GRB
import logging


def create_new_servings_vars(model,data):
    """"
    new_price[i]
    creates a new servings variable which denotes the number of servings  of the item[i] 
    type:
    continous
    """
    return [model.addVar(lb=0,ub=data.servings[i],vtype=GRB.INTEGER, name=f"servings{i}") for i in range(len(data.items))]
    logging.debug("new_servings variable is declared")


def min_req_calories(model, data, new_servings):
    """"
    this constarint denotes that manimum requirement of fat  is satisfied
    """
    model.addConstr(sum(new_servings[i]*data.calories[i] for i in range(len(data.items)))>=data.min_req["calories"])
    #model.addConstr(sum(new_servings[i]*data.calories[i] for i in range(len(data.items)))<=117)
    logging.debug("min_req_calories is used ")

def min_req_protein(model, data, new_servings):
    """"
    this constarint denotes that manimum requirement of protein  is satisfied
    """
    model.addConstr(sum(new_servings[i]*data.protein[i] for i in range(len(data.items)))>=data.min_req["protein"])
    #model.addConstr(sum(new_servings[i]*data.protein[i] for i in range(len(data.items)))<=117)
    logging.debug("min_req_protein is used ")

def min_req_fat(model, data, new_servings):
    """"
    this constarint denotes that manimum requirement of protein  is satisfied
    """
    model.addConstr(sum(new_servings[i]*data.Fat[i] for i in range(len(data.items)))>=data.min_req["fat"])
    #model.addConstr(sum(new_servings[i]*data.protein[i] for i in range(len(data.items)))<=117)
    logging.debug("min_req_protein is used ")

def min_req_carbohydrates(model, data, new_servings):
    """"
    this constarint denotes that manimum requirement of carbohydrates  is satisfied
    """
    model.addConstr(sum(new_servings[i]*data.carbohydrates[i] for i in range(len(data.items)))>=data.min_req["carbohydrates"])
    #model.addConstr(sum(new_servings[i]*data.carbohydrates[i] for i in range(len(data.items)))<=117)
    logging.debug("min_req_carbohydrates is used ")



def max_allowance_fat(model, data, new_servings):
    """"
    this constarint denotes that maximum requirement  of fat  is satisfied
    """
    model.addConstr(sum(new_servings[i]*data.Fat[i] for i in range(len(data.items)))<=data.max_allowance)
    logging.debug("max_req_fat is used ")

def set_objective_function(model, data, new_servings):
    """
    the objective is Minimize: the total cost of the menu,
    """
    logging.debug("constraint is used ")
    model.setObjective(sum(data.price[i] * new_servings[i] for i in range(len(data.items))), GRB.MINIMIZE)

def save_output(filename, content):
    """
    saves the output in aiims/output folder 
    
    """
    os.makedirs("diet_problem/outputs", exist_ok=True)
    with open(f"diet_problem/outputs/{filename}", "w") as file:
        file.write(content)

# def print_table(model, data,new_servings):
#     model.optimize()
#     if model.status == GRB.OPTIMAL:
#         output = 'Solution:\n'
#         output += f'Objective value = {model.objVal}\n\n'
#         #output += f'Best bound = {model.ObjBound}\n\n'
#         output += '{:<15} {:<15}\n'.format('Item', 'New servings' )
#         Food=data.items
#         for i, item in enumerate(Food):
#             output += '{:<15} {:<15.2f} \n'.format(item, new_servings[i].x)
#         return output
#     else:
#         return "No optimal solution found."


import csv
from gurobipy import GRB

def print_table(model, data, new_servings, filename='diet_problem/outputs/solution.csv'):
    model.optimize()
    
    if model.status == GRB.OPTIMAL:
        output = 'Solution:\n'
        output += f'Objective value = {model.objVal}\n\n'
        output += '{:<15} {:<15}\n'.format('Item', 'New servings')
        
        # Prepare data for output and CSV
        Food = data.items
        rows = []  # To hold rows for CSV
        
        for i, item in enumerate(Food):
            servings = new_servings[i].x
            output += '{:<15} {:<15.2f} \n'.format(item, servings)
            rows.append([item, servings])  # Add to rows for CSV
        rows.append(['Optimal Cost',model.objVal])

        # Save to CSV
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Item', 'New servings'])  # Header
            writer.writerows(rows)  # Data rows
            
        return output
    else:
        return "No optimal solution found."

