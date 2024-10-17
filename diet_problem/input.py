# input_data.py
import pandas as pd

class InputData:
    def __init__(self):
        self.load_data()

    def load_data(self):
        # Read nutritional data
        #nutritional_df = pd.read_excel('nutritional_data.xlsx')
        #self.fat = nutritional_df.set_index('Item')['Fat'].to_dict()
        #self.dry_matter = nutritional_df.set_index('Item')['Dry matter'].to_dict()
        #self.water = nutritional_df.set_index('Item')['Water'].to_dict()

        # Read demand and prices
        # Load user-edited nutrition data if available
        nutritions_df = pd.read_excel('diet_problem/nutrition_data.xlsx')
        # nutritions_df = pd.read_excel('AIIMS_CASE_STUDIES/diet_problem/nutrition_data.xlsx')
        nutrition_df=nutritions_df
        self.items=nutrition_df['Item']
        print(self.items)
        self.calories=nutrition_df['Calories (kcal)']
        self.protein=nutrition_df['Protein (gram)']
        self.Fat=nutrition_df['Fat (gram)']
        self.servings=nutrition_df['Max Servings']
        self.carbohydrates=nutrition_df['Carbohydrates (gram)']
        self.servings=nutrition_df['Max Servings']
        self.price=nutrition_df['Price (Hfl)']
        #self.allowance=nutrition_df['Maximum Allowance']
        #self.req=nutrition_df['Minimum Requirement']
        #self.max_allowance=117
        # self.max_allowance=nutritions_df.loc[nutritions_df['Item'] == 'Maximum Allowance', 'Fat (gram)'].values[0]
        # #self.max_allowance = nutritions_df.query("Item == 'Maximum Allowance'")['Fat (gram)']

        # print(self.max_allowance)
        # self.min_req={"calories":nutritions_df.loc[nutritions_df['Item'] == 'Minimum Requirement', 'Calories (kcal)'].values[0],
        #                "protein":nutritions_df.loc[nutritions_df['Item'] == 'Minimum Requirement', 'Protein (gram)'].values[0],
        #                "fat":nutritions_df.loc[nutritions_df['Item'] == 'Minimum Requirement', 'Fat (gram)'].values[0],
        #                "carbohydrates":nutritions_df.loc[nutritions_df['Item'] == 'Minimum Requirement', 'Carbohydrates (gram)'].values[0]}
    
