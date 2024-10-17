import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from Excel files
@st.cache
def load_excel_data(file_path):
    return pd.read_excel(file_path, sheet_name=None)  # Load all sheets as a dictionary of DataFrames

# Load specific files
shift_schedule = load_excel_data('employee_shift_details.xlsx')
holiday_requirement = load_excel_data('Holiday requirement.xlsx')
daily_requirement = load_excel_data('Daily requirement.xlsx')
employee_cost = pd.read_excel('Employee_cost.xlsx')

# Streamlit app interface
st.title("Employee Shift Optimization Results")

# Interactive Dashboard Layout
tabs = st.tabs(["Day-wise Results", "Overall Results"])

# Day-wise results
with tabs[0]:
    st.sidebar.header("Select a Day to View Results")
    selected_day = st.sidebar.selectbox("Select Day", options=list(shift_schedule.keys()))

    # Display shift schedule for the selected day
    st.header(f"Shift Schedule for Day {selected_day}")
    st.dataframe(shift_schedule[selected_day])

    # Display holiday requirement for the selected day
    st.header(f"Holiday Requirement for Day {selected_day}")
    st.dataframe(holiday_requirement[selected_day])

    # Display daily requirement for the selected day
    st.header(f"Daily Requirement for Day {selected_day}")
    st.dataframe(daily_requirement[selected_day])

# Overall results
with tabs[1]:
    st.header("Employee Cost Summary")
    st.dataframe(employee_cost)

    # Display dynamic summary metrics
    total_cost = employee_cost['Cost'].sum()
    total_shifts = employee_cost['number of shifts worked'].sum()
    st.metric("Total Employee Cost", f"${total_cost:,.2f}")
    st.metric("Total Number of Shifts Worked", total_shifts)

    # Visualization Options
    st.sidebar.header("Visualization Options")
    viz_option = st.sidebar.selectbox("Select Visualization Type", 
                                       ["Shift Distribution", "Total Cost per Employee", "Employee Shifts per Day", "Employee Cost Scatter Plot"])

    # Visualization
    if viz_option == "Shift Distribution":
        st.header("Shift Distribution per Employee")
        plt.figure(figsize=(10, 5))
        plt.bar(employee_cost['Employee ID'], employee_cost['number of shifts worked'], color='skyblue')
        plt.xlabel("Employee ID")
        plt.ylabel("Number of Shifts Worked")
        plt.title("Shift Distribution per Employee")
        st.pyplot(plt)

    elif viz_option == "Total Cost per Employee":
        st.header("Total Cost per Employee")
        plt.figure(figsize=(10, 5))
        plt.bar(employee_cost['Employee ID'], employee_cost['Cost'], color='salmon')
        plt.xlabel("Employee ID")
        plt.ylabel("Cost ($)")
        plt.title("Total Cost per Employee")
        st.pyplot(plt)

    elif viz_option == "Employee Shifts per Day":
        st.header("Employee Shifts per Day")
        shift_counts = {day: len(shift_schedule[day]) for day in shift_schedule.keys()}
        plt.figure(figsize=(10, 5))
        plt.plot(shift_counts.keys(), shift_counts.values(), marker='o', color='green')
        plt.xlabel("Day")
        plt.ylabel("Number of Shifts")
        plt.title("Total Employee Shifts per Day")
        st.pyplot(plt)

    elif viz_option == "Employee Cost Scatter Plot":
        st.header("Employee Cost vs. Number of Shifts Worked")
        plt.figure(figsize=(10, 5))
        plt.scatter(employee_cost['number of shifts worked'], employee_cost['Cost'], color='orange')
        for i in range(len(employee_cost)):
            plt.annotate(employee_cost['Employee ID'][i], (employee_cost['number of shifts worked'][i], employee_cost['Cost'][i]), fontsize=8)
        plt.xlabel("Number of Shifts Worked")
        plt.ylabel("Cost ($)")
        plt.title("Cost vs. Number of Shifts Worked")
        st.pyplot(plt)

    

st.sidebar.info("Use the sidebar to select day-wise results and visualization options.")
