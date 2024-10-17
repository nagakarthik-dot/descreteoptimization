## deciison_variables.py

from definitions import create_new_servings_vars

class DecisionVariables:
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.new_servings = None

    def create_variables(self):
        self.new_servings = create_new_servings_vars(self.model, self.data)
        
    def get_variables(self):
        return {
            'new_servings': self.new_servings
        }
