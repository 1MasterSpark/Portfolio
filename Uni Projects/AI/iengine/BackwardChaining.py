# BackwardChaining class for backward chaining algorithm
class BackwardChaining:
    def __init__(self, kb, query):
        self.kb = kb  # Knowledge base
        self.query = query  # Query symbol

    def bc_check(self):
        # Initialize goals with the query
        goals = [self.query]
        entailed = []  # List to store entailed symbols

        while goals:
            q = goals.pop()  # Get the last goal
            entailed.append(q)

            for clause in self.kb.get_clauses():
                if clause.consequent == q:
                    for antecedent in clause.antecedents:
                        if antecedent not in goals and antecedent not in entailed:
                            goals.append(antecedent)
            
            if all(clause.consequent != q for clause in self.kb.get_clauses()):
                return False, entailed  # Query is not entailed

        return True, entailed  # Query is entailed