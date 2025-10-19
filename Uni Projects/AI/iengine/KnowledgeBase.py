# Knowledge base class to hold clauses and symbols
class KnowledgeBase:
    def __init__(self):
        self.clauses = []  # List to store clauses
        self.symbols = set()  # Set to store unique symbols

    def add_clause(self, clause):
        # Add a clause to the knowledge base and update symbols
        self.clauses.append(clause)
        self.symbols.update(clause.antecedents)
        self.symbols.add(clause.consequent)  # Update() and add() both ensure there is are no duplicates

    def get_clauses(self):
        # Return all clauses in the knowledge base
        return self.clauses