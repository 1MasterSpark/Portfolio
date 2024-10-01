import sys
from KnowledgeBase import KnowledgeBase
from Clause import Clause
from TruthTable import TruthTable
from BackwardChaining import BackwardChaining
from ForwardChaining import ForwardChaining

# Function to parse the input file and create knowledge base and query
def parse_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    kb = KnowledgeBase()
    query = None
    parsing_kb = False
    
    for line in lines:
        line = line.strip()
        if line.startswith("TELL"):
            parsing_kb = True
            continue
        if line.startswith("ASK"):
            parsing_kb = False
            continue
        
        if parsing_kb:
            clauses = line.split(';')  # Split the clauses
            for clause in clauses:
                if '=>' in clause:
                    clause = clause.strip()
                    antecedents, consequent = clause.split('=>')
                    antecedents = antecedents.split('&')
                    for antecedent in antecedents:
                        antecedents[antecedents.index(antecedent)] = antecedent.strip()  # strip() removes whitespace before and after the symbol
                    kb.add_clause(Clause(antecedents, consequent.strip()))
                else:
                    if clause:
                        kb.add_clause(Clause([], clause.strip()))
        else:
            query = line
                    
    return kb, query

# Main function to execute the appropriate algorithm based on user input
def main():
    if len(sys.argv) < 3:
        print("Usage: python iengine.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].lower()  # This allows the method to be UPPERCASE, lowercase, or MiXeD

    kb, query = parse_file(filename)
    
    if method == 'tt':
        tt = TruthTable(kb, query)
        result, count = tt.tt_check_all()
        if result:
            print(f"YES: {count}")
        else:
            print("NO")
    elif method == 'fc':
        fc = ForwardChaining(kb, query)
        result, entailed = fc.fc_check()
        if result:
            print(f"YES: {', '.join(entailed)}")
        else:
            print("NO")
    elif method == 'bc':
        bc = BackwardChaining(kb, query)
        result, entailed = bc.bc_check()
        if result:
            print(f"YES: {', '.join(entailed)}")
        else:
            print("NO")
    else:
        print("Invalid method")

if __name__ == "__main__":
    main()