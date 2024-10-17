import gurobipy as gp
from gurobipy import GRB
import numpy as np
import csv
import pandas as pd

# ----------------- Parameters -----------------
min_value = 2      # Minimum employee requirement per hour
max_value = 7      # Maximum employee requirement per hour
days = 30         # Number of days
hours = 24 * days  # Total hours for scheduling
work_hours = 9     # Number of hours an employee works in a shift
employee_cost = 80 # Cost per employee per hour
shift_break = 12   # Break between two shifts in hours
num_employees = 30 # Total number of employees

# Generate random requirements for each hour within the specified range
requirement = np.random.randint(min_value, max_value + 1, size=hours)

# ----------------- Gurobi Model Initialization -----------------
model = gp.Model('Shift Scheduling')
model.setParam('MIPGap', 0.01)

# ----------------- Decision Variables -----------------
# Binary decision variables for work shifts and overnight shifts
work = {}         # Employee work shifts (binary)
overnight = {}    # Employee overnight shifts (binary)
work_day = {}     # Binary variable to track whether an employee works on a particular day (binary)

# Overnight shift variables
for day in range(days):
    overnight[day] = {}
    for employee in range(num_employees):
        overnight[day][employee] = model.addVar(vtype=GRB.BINARY, name=f'employee_{employee}_overnight_day{day}')

# Work shift variables
for employee in range(num_employees):
    for start in range(hours - work_hours + 1):  # Start time for shifts
        for end in range(start, start + work_hours):  # End time for shifts
            work[(employee, start, end)] = model.addVar(vtype=GRB.BINARY, name=f'employee_{employee}_start_{start}_end_{end}')

# Work day variables
for employee in range(num_employees):
    for day in range(days):
        work_day[(employee, day)] = model.addVar(vtype=GRB.BINARY, name=f'employee_{employee}_work_day_{day}')

# ----------------- Constraints -----------------
# 1. Ensure a 12-hour gap between shifts
for employee in range(num_employees):
    for start in range(hours - work_hours + 1):
        for next_start in range(start + 1, min(hours - work_hours + 1, start + work_hours + shift_break - 1)):
            model.addConstr(work[(employee, next_start, next_start)] + work[(employee, start, start)] <= 1)

# 2. Ensure total worked hours in a shift equals 8
for employee in range(num_employees):
    for start in range(hours - work_hours + 1):
        model.addConstr(gp.quicksum(work[(employee, start, end)] for end in range(start, start + work_hours)) == 8 * work[(employee, start, start)])

# 3. At least 2 of the 3 hours (3rd to 6th) must be worked
for employee in range(num_employees):
    for start in range(hours - work_hours + 1):
        model.addConstr(gp.quicksum(work[(employee, start, hour)] for hour in range(start + 3, start + 6)) == 2 * work[(employee, start, start)])

# 4. Overnight shifts are counted correctly
for employee in range(num_employees):
    for day in range(days):
        for hour in range(max(0, 24 * day - 7), 24 * day + 6):
            model.addConstr(overnight[day][employee] >= work[(employee, hour, hour)])

# 5. Meet hourly requirements
for hour in range(hours):
    model.addConstr(gp.quicksum(work[(employee, start, hour)] for employee in range(num_employees)
                                for start in range(hour - work_hours + 1, hour + 1)
                                if (employee, start, hour) in work) >= requirement[hour])

# 6. Ensure at least one and at most three holidays per employee
for employee in range(num_employees):
    # Ensure each employee works at least 12 and at most 14 days
    model.addConstr(gp.quicksum(work_day[(employee, day)] for day in range(days)) >= 27)  # Minimum 12 days worked
    model.addConstr(gp.quicksum(work_day[(employee, day)] for day in range(days)) <= 29)  # Maximum 14 days worked

# 7. Define work_day based on whether the employee works on a particular day
for employee in range(num_employees):
    for day in range(1,days-1):
        model.addConstr(gp.quicksum(work[(employee, start, end)] for start in range(day * 24, (day + 1) * 24 - work_hours + 1) for end in range(start, start + work_hours)) >= work_day[(employee, day)])
        # Ensure if no work in a day, then no work_day
        model.addConstr(gp.quicksum(work[(employee, start, end)] 
                                    for end in range(day * 24, (day + 1) * 24 ) 
                                    for start in range(max(0,end-8),min(hours,end+1))) <= 24 * work_day[(employee, day)])

# ----------------- Objective Function -----------------
# Minimize total cost (weighted cost of shifts and overnight shifts)
model.setObjective(
    10 * gp.quicksum(work[(employee, start, end)] for employee in range(num_employees)
                     for start in range(hours - work_hours + 1)
                     for end in range(start, start + work_hours)) +
    20 * gp.quicksum(overnight[day][employee] for day in range(days) for employee in range(num_employees)),
    GRB.MINIMIZE)

# ----------------- Model Optimization -----------------
model.optimize()

# ----------------- Output -----------------
# Check if the solution is optimal
if model.status == GRB.OPTIMAL:
    print(f'Optimal objective value (total cost): {model.objVal}')

    for i in range(num_employees):
        for d in range(days):
            if work_day[(i,d)].x<0.5:
                print(f'employee {i} holiday on day{d}')
    num_shifts=[0 for _ in range(num_employees)]
    # CSV Output for shift schedule
    with open('shift_schedule_output.csv', 'w', newline='') as csvfile:
        fieldnames = ['Employee', 'Day', 'Start Hour', 'Lunch Hour', 'End', 'Overnight']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Write the optimal shift schedule
        for employee in range(num_employees):
            for start in range(hours - work_hours + 1):
                if work[(employee, start, start)].x > 0.9:  # Check if employee starts work
                    num_shifts[employee]+=1
                    day = start // 24
                    overnight_flag = 1 if overnight[day][employee].x > 0.5 else 0
                    writer.writerow({
                        'Employee': employee,
                        'Day': day,
                        'Start Hour': start % 24,
                        'Lunch Hour': (start + 4) % 24,
                        'End': (start + 8) % 24,
                        'Overnight': overnight_flag
                    })

    print('Shift schedule saved to shift_schedule_output.csv')

    # CSV Output for daily requirements and employee count
    employee_schedule = [[] for _ in range(hours)]
    with open('shift_schedule_peroutput.csv', 'w', newline='') as csvfile:
        fieldnames = ['Day', 'Hour', 'Requirement', 'Working Employees', 'Count of Employees Working', 'Extra']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for employee in range(num_employees):
            for start in range(hours - work_hours + 1):
                for end in range(start, start + work_hours):
                    if work[(employee, start, end)].x > 0.5:
                        employee_schedule[end].append(employee)

        for hour in range(hours):
            day = hour // 24
            writer.writerow({
                'Day': day,
                'Hour': hour % 24,
                'Requirement': requirement[hour],
                'Working Employees': employee_schedule[hour],
                'Count of Employees Working': len(employee_schedule[hour]),
                'Extra': len(employee_schedule[hour]) - requirement[hour]
            })

    print('Daily requirements saved to shift_schedule_peroutput.csv')

    # Excel Output for detailed employee shift data
    shift_data = {day: [] for day in range(days)}
    num_shifts = [0 for _ in range(num_employees)]

    for employee in range(num_employees):
        for start in range(hours - work_hours + 1):
            if work[(employee, start, start)].x > 0.9:
                day = start // 24
                num_shifts[employee] += 1
                overnight_flag = 1 if overnight[day][employee].x > 0.5 else 0
                shift_data[day].append({
                    'Employee_id': employee,
                    'Start Hour': start % 24,
                    'Break Hour': (start + 4) % 24,
                    'End Hour': (start + 8) % 24,
                    'Overnight': overnight_flag
                })

    with pd.ExcelWriter('employee_shift_details.xlsx') as writer:
        for day in range(days):
            df = pd.DataFrame(shift_data[day])
            df.to_excel(writer, sheet_name=f'Day_{day + 1}', index=False)

    print('Employee shift details saved to employee_shift_details.xlsx')

    # Excel Output for daily requirement details
    shift_data1 = {day: [] for day in range(days)}
    employee_schedule = [[] for _ in range(hours)]
    

    for employee in range(num_employees):
        for start in range(hours - 8):
            for end in range(start, start + 9):
                if work[(employee, start, end)].x > 0.5:
                    employee_schedule[end].append(employee)

    for hour in range(hours):
        day = hour // 24
        res=[]
        for i in range(num_employees):
            if work_day[(i,day)].x<0.5:
                res.append(i)
        shift_data1[day].append({
            'Hour': hour % 24,
            'Requirement': requirement[hour],
            'Working Employees': employee_schedule[hour],
            'Number of Employees Working': len(employee_schedule[hour])
            #'employee on holiday':res
        })
    extraaa={day: [] for day in range(days)}
    for day in range(days):
        for i in range(num_employees):
            if work_day[(i,day)].x<=0.5:
                extraaa[day].append(i)
    with pd.ExcelWriter('Holiday requirement.xlsx') as writer:
        for day in range(days):
            df = pd.DataFrame(extraaa[day],columns=['id'])
            df.to_excel(writer, sheet_name=f'Day_{day + 1}', index=False)
    
    with pd.ExcelWriter('Daily requirement.xlsx') as writer:
        for day in range(days):
            df = pd.DataFrame(shift_data1[day])
            df.to_excel(writer, sheet_name=f'Day_{day + 1}', index=False)


    print('Daily requirement saved to Daily requirement.xlsx')

    # Excel Output for employee cost data
    cost_data = []
    for employee in range(num_employees):
        total_cost = (
            10 * gp.quicksum(work[(employee, start, end)].x for start in range(hours - work_hours + 1) for end in range(start, start + work_hours)) +
            20 * gp.quicksum(overnight[day][employee].x for day in range(days))
        )
        cost_data.append({
            'Employee ID': employee,
            'Cost': total_cost,
            'number of shifts worked':num_shifts[employee]
        })

    df = pd.DataFrame(cost_data)
    df.to_excel('Employee_cost.xlsx', index=False)
    print('Employee cost saved to Employee_cost.xlsx')

else:
    print('Optimal solution not found.')
