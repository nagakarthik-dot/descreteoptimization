


import streamlit as st
import pandas as pd
import os
import subprocess
from input import InputData

def load_data():
    """Load the input data for the optimization problem."""
    data = InputData()
    return data

def display_input_data(data):
    """Display the input data in a table format and allow modifications."""
    st.subheader("Input Data")
    nutrition_df = pd.DataFrame({
        'Item': data.items,
        'Calories (kcal)': data.calories,
        'Protein (gram)': data.protein,
        'Fat (gram)': data.Fat,
        'Carbohydrates (gram)': data.carbohydrates,
        'Max Servings': data.servings,
        'Price (Hfl)': data.price

    })
    # # Create a separate table for max allowance and min requirements
    # allowances_df = pd.DataFrame({
    #     'Description': ['Max Allowance for Fat', 'Min Calories requirement(cal)', 'Min Protein requirement(cal) ', 'Min Carbohydrates requiremnt (cal)'],
    #     'Value': [data.max_allowance, data.min_req["calories"], data.min_req["protein"], data.min_req["carbohydrates"]]
    # })

    # st.subheader("Nutritional Requirements")
    # st.table(allowances_df)

    # Allow user to modify the data in an editable table
    modified_nutrition_df = st.data_editor(nutrition_df, num_rows="dynamic")

    # Button to save the modified data
    if st.button("Save Modified Data"):
        modified_nutrition_df.to_excel('diet_problem/nutrition_data_modified.xlsx', index=False)
        st.success("Modified data saved successfully!")
    
    return modified_nutrition_df

def run_optimization():
    """Run the optimization script."""
    try:
        # Run the main.py script
        subprocess.run(["C:/Users/olw09/.pyenv/pyenv-win/versions/3.11.3/python.exe", "C:/Users/olw09/final/descreteoptimization/diet_problem/main.py"], check=True)
        st.success("Optimization completed successfully.")
    except subprocess.CalledProcessError as e:
        st.error(f"Error in optimization: {e}")

def display_output_data():
    st.write("The objective is to minimize the total cost of the menu")
    output_file_path = 'diet_problem/outputs/solution.csv'
    if os.path.exists(output_file_path):
        # Read the CSV file into a DataFrame
        output_df = pd.read_csv(output_file_path)
        
        st.subheader("Optimization Output")
        # Display the DataFrame as a table
        st.table(output_df)
    else:
        st.error("No output file found. Please run the optimization first.")

def main():
    st.title("Diet Optimization Dashboard")

    # Load input data
    data = load_data()

    # Display input data
    modified_nutrition_df = display_input_data(data)

    # Button to run the optimization
    if st.button("Run Optimization"):
        run_optimization()
        display_output_data()

if __name__ == "__main__":
    main()
