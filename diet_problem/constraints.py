# constraints.py

from definitions import *

class Constraints:
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.new_servings=None
    def add_constraints(self, new_servings):
        min_req_calories(self.model, self.data, new_servings)
        min_req_protein(self.model, self.data, new_servings)
        min_req_fat(self.model, self.data, new_servings)
        min_req_carbohydrates(self.model, self.data, new_servings)
        max_allowance_fat(self.model, self.data, new_servings)

        