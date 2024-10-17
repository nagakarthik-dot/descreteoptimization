# results.py
from input_data import *
from definitions import print_table, save_output

class FinalTable:
    def __init__(self, model,data, variables):
        self.model = model
        self.data=data
        self.new_servings = variables['new_servings']
        

    def print_table(self):
        return print_table(self.model,self.data, self.new_servings,filename='diet_problem/outputs/solution.csv')

    def save_output(self, filename, content):
        save_output(filename, content)
