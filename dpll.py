from Rezolutie import create_matrix_from_file, remove_trivial_clauses
from DP import is_unit_clause, is_pure_literal, unit_propagation, remove_pure_literal, has_clauses
from collections import Counter
import copy, time, psutil, os

def find_split_literal(clauses):
    literal_frequency = Counter()

    for clause in clauses:
        for literal in clause:
            literal_frequency[abs(literal)] += 1

    return literal_frequency.most_common(1)[0][0]

def is_SAT_DPLL(clauses):

    while has_clauses(clauses):

        while is_unit_clause(clauses):
            clauses = unit_propagation(clauses)

        if not has_clauses(clauses):
            return True

        if [] in clauses:
            return False

        while is_pure_literal(clauses):
            literal_to_remove = is_pure_literal(clauses)
            clauses = remove_pure_literal(clauses, literal_to_remove)

        if not has_clauses(clauses):
            return True

        split_literal = find_split_literal(clauses)

        clauses1 = copy.deepcopy(clauses)
        clauses1.append([split_literal])

        clauses2 = copy.deepcopy(clauses)
        clauses2.append([-split_literal])

        return is_SAT_DPLL(clauses1) or is_SAT_DPLL(clauses2)

    return True

start = time.time()

matrix = create_matrix_from_file(r"./clauses.cnf")

matrix = remove_trivial_clauses(matrix)

if is_SAT_DPLL(matrix):
    print("The clauses are SATISFIABLE")
else:
    print("The clauses are UNSATISFIABLE")

process = psutil.Process(os.getpid())
memory_info = process.memory_info()
print(f"Memory consumed: {memory_info.rss}B")
print(f"Memory consumed: {memory_info.rss / 1024:.2f}KB")
print(f"Memory consumed: {memory_info.rss / (1024**2):.2f}MB")
print(f"Memory consumed: {memory_info.rss / (1024**3):.2f}GB")

end = time.time()
elapsed_time = (end - start)
print(f"Total execution time: {elapsed_time:.3f} seconds")
