# ForwardChaining class for forward chaining algorithm
class ForwardChaining:
    def __init__(self, kb, query):
        self.kb = kb  # Knowledge base
        self.query = query  # Query symbol

    def fc_check(self):
        # Initialize agenda with facts (clauses with no antecedents)
        agenda = [clause.consequent for clause in self.kb.get_clauses() if not clause.antecedents]
        entailed = []  # List to store entailed symbols

        while agenda:
            p = agenda.pop(0)  # Get the first symbol from the agenda
            entailed.append(p)

            for clause in self.kb.get_clauses():
                if p in clause.antecedents:
                    if all(antecedent in entailed for antecedent in clause.antecedents):
                        agenda.append(clause.consequent)

            if p == self.query:
                return True, entailed  # Query is entailed

        return False, []  # Query is not entailed