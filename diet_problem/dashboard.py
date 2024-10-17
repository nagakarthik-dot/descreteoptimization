import streamlit as st
import pandas as pd
import os
import openpyxl
import subprocess
import sys
from input import InputData

def load_data():
    """Load the input data for the optimization problem."""
    data = InputData()
    return data

def display_input_data(data):
    """Display the input data in a table format and allow modifications."""
    st.subheader("Input Data")

    if 'nutrition_df' not in st.session_state:
        st.session_state['nutrition_df'] = pd.DataFrame({
            'Item': data.items,
            'Calories (kcal)': data.calories,
            'Protein (gram)': data.protein,
            'Fat (gram)': data.Fat,
            'Carbohydrates (gram)': data.carbohydrates,
            'Max Servings': data.servings,
            'Price (Hfl)': data.price
        })

    nutrition_df = st.session_state['nutrition_df']

    # Button to "Add New Row" form
    with st.expander("Add New Row", expanded=False):
        with st.form("add_row_form", clear_on_submit=True):
            new_item = st.text_input("Item")
            new_calories = st.number_input("Calories (kcal)", value=0.0)
            new_protein = st.number_input("Protein (gram)", value=0.0)
            new_fat = st.number_input("Fat (gram)", value=0.0)
            new_carbohydrates = st.number_input("Carbohydrates (gram)", value=0.0)
            new_servings = st.number_input("Max Servings", value=0)
            new_price = st.number_input("Price (Hfl)", value=0.0)
            submitted = st.form_submit_button("Add Row")

            # If form is submitted, add the new row to the DataFrame
            if submitted:
                new_row = {
                    'Item': new_item,
                    'Calories (kcal)': new_calories,
                    'Protein (gram)': new_protein,
                    'Fat (gram)': new_fat,
                    'Carbohydrates (gram)': new_carbohydrates,
                    'Max Servings': new_servings,
                    'Price (Hfl)': new_price
                }
                st.session_state['nutrition_df'] = pd.concat([ pd.DataFrame([new_row]),nutrition_df], ignore_index=True)
                st.success("New row added successfully!")

    # Allow user to modify the data in an editable table
    modified_nutrition_df = st.data_editor(st.session_state['nutrition_df'], num_rows="dynamic")

    # Button to save the modified data
    if st.button("Save Modified Data"):
        modified_nutrition_df.to_excel('diet_problem/nutrition_data_modified.xlsx', index=False)
        st.success("Modified data saved successfully!")

    return modified_nutrition_df

def run_optimization():
    """Run the optimization script."""
    try:
        # Run the main.py script
        subprocess.run(["C:/Users/olw09/.pyenv/pyenv-win/versions/3.11.3/python.exe", "diet_problem/main.py"], check=True)
        #subprocess.run([sys.executable, "diet_problem/main.py"], check=True)
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
        st.error("No output file found. Please run the optimization first or model doesn't have an optimal solution .")

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

