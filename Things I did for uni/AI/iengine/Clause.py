# Clause class to represent a logical clause
class Clause:
    def __init__(self, antecedents, consequent):
        self.antecedents = antecedents  # List of antecedent symbols
        self.consequent = consequent  # Consequent symbol