from Clause import Clause

# TruthTable class for truth table algorithm
class TruthTable:
    def __init__(self, kb, query):
        self.kb = kb  # Knowledge base
        self.query = query  # Query symbol

    def tt_check_all(self):
        # Check all models for satisfiability of the query
        symbols = list(self.kb.symbols)
        return self._tt_check_all(symbols, {})

    def _tt_check_all(self, symbols, model):
        # Recursively check all models
        if not symbols:
            if self._pl_true(self.kb.get_clauses(), model):
                return self._pl_true([self.query], model), 1
            else:
                return True, 0

        first, rest = symbols[0], symbols[1:]
        model_true = model.copy()
        model_true[first] = True
        model_false = model.copy()
        model_false[first] = False

        true_count = self._tt_check_all(rest, model_true)
        false_count = self._tt_check_all(rest, model_false)

        return (true_count[0] and false_count[0]), true_count[1] + false_count[1]

    def _pl_true(self, clauses, model):
        # Check if clauses are true in the given model
        for clause in clauses:
            if isinstance(clause, Clause):
                antecedents_true = all(model.get(ant, False) for ant in clause.antecedents)
                consequent_true = model.get(clause.consequent, False)
                if antecedents_true and not consequent_true:
                    return False
            else:
                if not model.get(clause, False):
                    return False
        return True