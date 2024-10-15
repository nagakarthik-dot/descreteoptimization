import gurobipy as gp
from gurobipy import GRB
import numpy as np
import csv

# Constants for the problem
min_value = 2      # Minimum employee requirement per hour
max_value = 7      # Maximum employee requirement per hour
days=15    # num of days 
hour = 24*days      # Total hours for scheduling
work_hours = 9     # Number of hours an employee works in a shift
employee_cost = 80 # Cost per employee per hour
overnight_cost=20
shift_break=12     # break between two shifts 
# Generate random requirements for each hour within the specified range
requirement = np.random.randint(min_value, max_value + 1, size=hour)

num_employees = 30 # Total number of employees
model = gp.Model('Shift Scheduling') # Create a new Gurobi model for shift scheduling
model.setParam('MIPGap', 0.01) 
# Decision variables
work = {}         # Binary decision variables for employee work shifts
overnight = {}    # Integer decision variables for overnight shifts

# Create decision variables for overnight shifts for 2 types (day and night)
for i in range(days):
    overnight[i]={}
    for j in range(num_employees):
        overnight[i][j] = model.addVar(vtype=GRB.BINARY, name=f'employee_{j}_works_overnight on day{i}')

# Create binary decision variables for work shifts
for i in range(num_employees):   
    for j in range(hour - work_hours +1):  # Start time for shifts
        for k in range(j, j + work_hours):  # End time for shifts
            work[(i, j, k)] = model.addVar(vtype=GRB.BINARY, name=f'employee_{i}_start_{j}_work_{k}')

# Constraints

# Ensure a 12-hour gap between shifts
for i in range(num_employees):
    for j in range(hour - work_hours + 1):
        for k in range(j + 1, min(hour-work_hours+1,j + work_hours+shift_break-1)):  # Check the next 20 hours
            model.addConstr(work[(i, k, k)] + work[(i, j, j)] <= 1)  # No overlap in shifts

# Ensure that the total worked hours in a shift equals 8
for i in range(num_employees):
    for j in range(hour - work_hours + 1):
        model.addConstr(gp.quicksum(work[(i, j, k)] for k in range(j, j + work_hours)) == 8 * work[(i, j, j)])

# Ensure that during a shift, at least 2 of the 3 hours (3rd to 6th) are worked
for i in range(num_employees):
    for j in range(hour - work_hours + 1):
        model.addConstr(gp.quicksum(work[(i, j, k)] for k in range(j + 3, j + 6)) == 2 * work[(i, j, j)])


# # Ensure overnight shifts are counted correctly
for i in range(num_employees):
    for k in range(days):
        for j in range(max(0, 24 * k - 7), 24 * k + 6):
            model.addConstr(overnight[k][i] >= work[i, j, j])  # Count overnight shifts

# Requirement satisfaction constraints
for k in range(hour):
    model.addConstr(gp.quicksum(work[(i, j, k)] for i in range(num_employees)
                                for j in range( k - work_hours + 1, k + 1)
                                if (i, j, k) in work) >= requirement[k])  # Meet hourly requirements

# Objective Function
model.setObjective(
    employee_cost/8 * (gp.quicksum(work[(i, j, k)] for i in range(num_employees)
                      for j in range(hour - work_hours + 1)
                      for k in range(j, j + work_hours))) +
     overnight_cost * (gp.quicksum(overnight[k][i] for k in range(days) for i in range(num_employees))),
    GRB.MINIMIZE)  # Minimize total cost of scheduling

# Optimize the model
model.optimize()

# Check if the solution is optimal
if model.status == GRB.OPTIMAL:
    print(f'Optimal objective value (total cost): {model.objVal}')
    
    # Prepare data for CSV output
    with open('shift_schedule_output.csv', 'w', newline='') as csvfile:
        fieldnames = ['Employee','Day', 'Start Hour', 'Lunch Hour','End', 'Overnight']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Write the optimal shift schedule to the CSV
        for i in range(num_employees):
         # Determine if the employee works overnight
            for j in range(hour - work_hours + 1):
                if work[(i, j, j)].x > 0.9:  # Check if the employee starts work at hour j
                    for k in range(j, j + work_hours):  # Record the working hours
                        day=k//24
                        overnight_flag=1 if overnight[day][i].x>0.5 else 0
                        if work[(i, j, k)].x < 0.5:
                            writer.writerow({
                            'Employee': i,
                            'Day':day,
                            'Start Hour': j,
                            'Lunch Hour': k,
                            'End' : j+8,
                            'Overnight': overnight_flag
                        })
    print('Output saved to shift_schedule_output.csv')  # Indicate successful CSV writing

    with open('shift_schedule_peroutput.csv', 'w', newline='') as csvfile:
        fieldnames = ['day', 'Hour', 'Requirement','working_employees', 'count of employee working','extra']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        employee = [[] for _ in range(hour)] 
        # Write the optimal shift schedule to the CSV
        for i in range(num_employees):
            for j in range(hour-8):
                for k in range(j,j+9):
                    if work[(i,j,k)].x>0.5:
                        employee[k].append(i)
        for k in range(hour):
            writer.writerow({
                'day' :k//24,
                'Hour':k,
                'Requirement': requirement[k],
                'working_employees': employee[k],
                'count of employee working':len(employee[k]),
                'extra': len(employee[k])-requirement[k]
            })

else:
    print('No optimal solution found.')  # Indicate if no optimal solution was found






import pandas as pd

# Initialize a dictionary to hold data for each day
shift_data = {day: [] for day in range(days)}  # Assuming a 7-day week
num_shifts=[0 for _ in range(num_employees)]
num_overnight=[0 for _ in range(num_employees)]
# Process the optimal shift schedule
for i in range(num_employees):
    for j in range(hour - work_hours + 1):
        if work[(i, j, j)].x > 0.9:  # Check if the employee starts work at hour j
            num_shifts[i]+=1
            overnight_flag = 1 if overnight[day][i].x > 0.5 else 0
            #num_overnight[i]+=overnight_flag
            for k in range(j, j + work_hours):  # Record the working hours
                day = k // 24
                overnight_flag = 1 if overnight[day][i].x > 0.5 else 0
                if work[(i, j, k)].x < 0.5:
                    # Append the shift data for the employee on the current day
                    shift_data[day].append({
                        'Employee_id': i,
                        'Start Hour of employee': j%24,
                        'Break Hour of employee': k%24,
                        'Ending hour of employee': (j + 8)%24,
                        'employee working Overnight': overnight_flag
                    })

# Create an Excel writer object
with pd.ExcelWriter('employee_shift_details.xlsx') as writer:
    # Write each day's data into a separate sheet
    for day in range(days):  
        # Convert the shift data to a DataFrame
        df = pd.DataFrame(shift_data[day])
        # Write to an Excel sheet with the day as the sheet name
        df.to_excel(writer, sheet_name=f'Day_{day + 1}', index=False)

print('Output saved to employee_shift_details.xlsx')

import pandas as pd

# Initialize a dictionary to hold data for each day
shift_data1 = {day: [] for day in range(days)}  # Assuming a 7-day week

employee = [[] for _ in range(hour)]

# Process the optimal shift schedule
for i in range(num_employees):
    for j in range(hour - 8):
        for k in range(j, j + 9):
            if work[(i, j, k)].x > 0.5:
                employee[k].append(i)

# Organize data into day-wise format
for k in range(hour):
    day = k // 24
    shift_data1[day].append({
        'Hour': k % 24,  # Only showing the hour within the day
        'Requirement': requirement[k],
        'working_employees_id': employee[k],
        'Number of employees working': len(employee[k])
        #'extra': len(employee[k]) - requirement[k]
    })

# Create an Excel writer object
with pd.ExcelWriter('Daily requirement.xlsx') as writer:
    # Write each day's data into a separate sheet
    for day in range(days):  # Assuming 7 days
        # Convert the shift data to a DataFrame
        df = pd.DataFrame(shift_data1[day])
        # Write to an Excel sheet with the day as the sheet name
        df.to_excel(writer, sheet_name=f'Day_{day + 1}', index=False)

print('Output saved to Daily requirement.xlsx')


import pandas as pd
cost_data = []

# Process the optimal shift schedule
for i in range(num_employees):
    total_cost = (
        10 * gp.quicksum(work[(i, j, k)].x for j in range(hour - work_hours + 1) for k in range(j, j + work_hours))
        + 20 * gp.quicksum(overnight[k][i].x for k in range(days))
    )
    
    # Append a dictionary with employee and their calculated cost
    cost_data.append({
        'employee_id': i,
        'cost of hiring': total_cost,
        'number of shifts worked':num_shifts[i]
       # 'number of overnight shifts':num_overnight[i]

    })

# Create a DataFrame from the cost data
df = pd.DataFrame(cost_data)

# Create an Excel writer object
with pd.ExcelWriter('shift_schedule_cost.xlsx') as writer:
    # Write the data to an Excel sheet
    df.to_excel(writer, index=False)

print('Output saved to shift_schedule_cost.xlsx')