# # dashboard.py
# import streamlit as st
# import pandas as pd
# import os
# import subprocess
# from input_data import InputData
import subprocess
import sys

# Function to install a package
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install openpyxl
install_package("pandas openpyxl")

# Now you can import and use openpyxl
import openpyxl

# Your code that uses openpyxl here

# def load_data():
#     """Load the input data for the optimization problem."""
#     data = InputData()
#     return data

# def display_input_data(data):
#     """Display the input data in a table format."""
#     st.subheader("Input Data")
#     nutrition_df = pd.DataFrame({
#         'Item': data.items,
#         'Calories (kcal)': data.calories,
#         'Protein (g)': data.protein,
#         'Fat (g)': data.Fat,
#         'Carbohydrates (g)': data.carbohydrates,
#         'Max Servings': data.servings,
#         'Price (Hfl)': data.price
#     })
#     st.table(nutrition_df)

#     # Create a separate table for max allowance and min requirements
#     allowances_df = pd.DataFrame({
#         'Description': ['Max Allowance for Fat', 'Min Calories requirement(cal)', 'Min Protein requirement(cal) ', 'Min Carbohydrates requiremnt (cal)'],
#         'Value': [data.max_allowance, data.min_req["calories"], data.min_req["protein"], data.min_req["carbohydrates"]]
#     })

#     st.subheader("Nutritional Requirements")
#     st.table(allowances_df)

# def run_optimization():
#     """Run the optimization script."""
#     try:
#         # Run the main.py script
#         subprocess.run(["python", "main.py"], check=True)
#         st.success("Optimization completed successfully.")
#     except subprocess.CalledProcessError as e:
#         st.error(f"Error in optimization: {e}")

# def display_output_data():
#     st.write("the objective is Minimize: the total cost of the menu")
#     output_file_path = 'AIIMS_CASE_STUDIES/diet_problem/outputs/solution.csv'
#     if os.path.exists(output_file_path):
#         # Read the CSV file into a DataFrame
#         output_df = pd.read_csv(output_file_path)
        
#         st.subheader("Optimization Output")
#         # Display the DataFrame as a table
#         st.table(output_df)
#     else:
#         st.error("No output file found. Please run the optimization first.")

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# def display_nutritional_charts(data):
#     """Display charts for nutritional data."""
#     st.subheader("Nutritional Composition")

#     # Create a DataFrame for plotting
#     nutrition_data = pd.DataFrame({
#         'Item': data.items,
#         'Calories (kcal)': data.calories,
#         'Protein (g)': data.protein,
#         'Fat (g)': data.Fat,
#         'Carbohydrates (g)': data.carbohydrates
#     })

#     # Bar chart for nutritional values
#     nutrition_data.set_index('Item').plot(kind='bar', figsize=(10, 6))
#     plt.title('Nutritional Composition of Food Items')
#     plt.ylabel('Nutritional Value')
#     plt.xticks(rotation=45)
#     st.pyplot(plt)

#     # Pie chart for maximum servings
#     st.subheader("Max Servings Distribution")
#     pie_data = nutrition_data.set_index('Item')['Max Servings']
#     st.write(pie_data)
#     st.write("Total Servings: ", pie_data.sum())
#     st.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)

#     # Add more charts as needed

# def display_output_data():
#     st.write("The objective is to minimize the total cost of the menu.")
#     output_file_path = 'AIIMS_CASE_STUDIES/diet_problem/outputs/solution.csv'
#     if os.path.exists(output_file_path):
#         output_df = pd.read_csv(output_file_path)
#         st.subheader("Optimization Output")
#         st.table(output_df)

#         # Download button
#         st.download_button(
#             label="Download Solution as CSV",
#             data=output_df.to_csv(index=False),
#             file_name='solution.csv',
#             mime='text/csv'
#         )
#     else:
#         st.error("No output file found. Please run the optimization first.")


# def main():
#     st.title("Diet Optimization Dashboard")

#     # Load input data
#     data = load_data()

#     # Display input data
#     display_input_data(data)

#     # Button to run the optimization
#     if st.button("Run Optimization"):
#         run_optimization()
#         display_output_data()



# if __name__ == "__main__":
#     main()

# import streamlit as st
# import pandas as pd
# import os
# import subprocess
# from input import InputData

# def load_data():
#     """Load the input data for the optimization problem."""
#     data = InputData()
#     return data

# def display_input_data(data):
#     """Display the input data in a table format and allow modifications."""
#     st.subheader("Input Data")
#     nutrition_df = pd.DataFrame({
#         'Item': data.items,
#         'Calories (kcal)': data.calories,
#         'Protein (gram)': data.protein,
#         'Fat (gram)': data.Fat,
#         'Carbohydrates (gram)': data.carbohydrates,
#         'Max Servings': data.servings,
#         'Price (Hfl)': data.price
#     })

#     # Allow user to modify the data
#     modified_nutrition_df = nutrition_df.copy()
#     for i in range(len(nutrition_df)):
#         st.write(f"Item: {nutrition_df['Item'].iloc[i]}")
#         modified_nutrition_df.at[i, 'Calories (kcal)'] = st.number_input(f"Calories (kcal) for {nutrition_df['Item'].iloc[i]}:", value=nutrition_df['Calories (kcal)'].iloc[i])
#         modified_nutrition_df.at[i, 'Protein (gram)'] = st.number_input(f"Protein (gram) for {nutrition_df['Item'].iloc[i]}:", value=nutrition_df['Protein (gram)'].iloc[i])
#         modified_nutrition_df.at[i, 'Fat (gram)'] = st.number_input(f"Fat (gram) for {nutrition_df['Item'].iloc[i]}:", value=nutrition_df['Fat (gram)'].iloc[i])
#         modified_nutrition_df.at[i, 'Carbohydrates (gram)'] = st.number_input(f"Carbohydrates (gram) for {nutrition_df['Item'].iloc[i]}:", value=nutrition_df['Carbohydrates (gram)'].iloc[i])
#         modified_nutrition_df.at[i, 'Max Servings'] = st.number_input(f"Max Servings for {nutrition_df['Item'].iloc[i]}:", value=nutrition_df['Max Servings'].iloc[i])
#         modified_nutrition_df.at[i, 'Price (Hfl)'] = st.number_input(f"Price (Hfl) for {nutrition_df['Item'].iloc[i]}:", value=nutrition_df['Price (Hfl)'].iloc[i])
    
#     # Save the modified data
#     if st.button("Save Modified Data"):
#         modified_nutrition_df.to_excel('AIIMS_CASE_STUDIES/diet_problem/nutrition_data_modified.xlsx', index=False)
#         st.success("Modified data saved successfully!")

# def run_optimization():
#     """Run the optimization script."""
#     try:
#         # Run the main.py script
#         subprocess.run(["C:/Users/olw09/.pyenv/pyenv-win/versions/3.11.3/python.exe", "c:/Users/olw09/shift/AIIMS_CASE_STUDIES/diet_problem/main.py"], check=True)

#         st.success("Optimization completed successfully.")
#     except subprocess.CalledProcessError as e:
#         st.error(f"Error in optimization: {e}")

# def display_output_data():
#     st.write("The objective is to minimize the total cost of the menu")
#     output_file_path = 'AIIMS_CASE_STUDIES/diet_problem/outputs/solution.csv'
#     if os.path.exists(output_file_path):
#         # Read the CSV file into a DataFrame
#         output_df = pd.read_csv(output_file_path)
        
#         st.subheader("Optimization Output")
#         # Display the DataFrame as a table
#         st.table(output_df)
#     else:
#         st.error("No output file found. Please run the optimization first.")

# def main():
#     st.title("Diet Optimization Dashboard")

#     # Load input data
#     data = load_data()

#     # Display input data
#     display_input_data(data)

#     # Button to run the optimization
#     if st.button("Run Optimization"):
#         run_optimization()
#         display_output_data()

# if __name__ == "__main__":
#     main()
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

