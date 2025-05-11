from Rezolutie import create_matrix_from_file, remove_trivial_clauses, combine_clauses
import copy, time, psutil, os

def is_unit_clause(clause_list):
    for clause in clause_list:
        if len(clause) == 1:
            return True
    return False

def is_pure_literal(clause_list):
    occurrences = {}
    for clause in clause_list:
        for literal in clause:
            if literal not in occurrences:
                occurrences[literal] = True
    for literal in occurrences:
        if -literal not in occurrences:
            return literal
    return False

def has_clauses(clause_list):
    if clause_list == []:
        return False
    return True

def unit_propagation(clause_list):
    literal_found = None
    for clause in clause_list:
        if len(clause) == 1:
            literal_found = clause[0]
            break
    new_clauses = []
    for clause in clause_list:
        if literal_found in clause:
            continue
        else:
            new_clause = [literal for literal in clause if literal != -literal_found]
            new_clauses.append(new_clause)
    return new_clauses

def remove_pure_literal(clause_list, pure_literal):
    new_clauses = []
    for clause in clause_list:
        if pure_literal in clause:
            continue
        else:
            new_clauses.append(clause)
    return new_clauses

def apply_resolution(clause_list):
    new_clauses = []
    for i in range(len(clause_list) - 1):
        for j in range(i + 1, len(clause_list)):
            new_clause = combine_clauses(clause_list[i], clause_list[j])
            if new_clause == []:
                return False
            elif new_clause != False:
                if new_clause not in clause_list and new_clause not in new_clauses:
                    new_clauses.append(new_clause)
    if new_clauses != []:
        clause_list.extend(new_clauses)
        return clause_list
    else:
        return True

def is_SAT_DP(clause_list):
    while has_clauses(clause_list):
        while is_unit_clause(clause_list):
            clause_list = unit_propagation(clause_list)

        if not has_clauses(clause_list):
            return True

        if [] in clause_list:
            return False

        while is_pure_literal(clause_list):
            pure_literal = is_pure_literal(clause_list)
            clause_list = remove_pure_literal(clause_list, pure_literal)

        if not has_clauses(clause_list):
            return True

        clause_list = apply_resolution(clause_list)

        if clause_list == True:
            return True

        elif clause_list == False:
            return False
    return True

start = time.time()

matrix = create_matrix_from_file(r"./clauses.cnf")

matrix = remove_trivial_clauses(matrix)

if is_SAT_DP(matrix):
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
