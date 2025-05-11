import time, os, psutil

def load_clauses(input_file):
    clauses = []

    with open(input_file, 'r') as file:
        for line in file:
            values = line.strip().split()
            sorted_clause = sorted([int(val) for val in values])
            clauses.append(sorted_clause)

    return clauses

def contains_opposite_literals(clause):
    literals = set(clause)

    for literal in literals:
        if -literal in literals:
            return True

    return False

def remove_trivial_clauses(clauses):
    return [clause for clause in clauses if not contains_opposite_literals(clause)]

def resolve_clauses(clause1, clause2):
    result = []
    literals_added = False
    literal_used_for_resolution = None

    for literal in clause1:
        if -literal in clause2 and not literals_added:
            literals_added = True
            literal_used_for_resolution = -literal
            continue
        else:
            result.append(literal)

    for literal in clause2:
        if literal not in result and literal != literal_used_for_resolution:
            result.append(literal)

    for i in range(len(result) - 1):
        for j in range(i + 1, len(result)):
            if result[i] == -result[j]:
                return False

    if len(result) <= max(len(clause1), len(clause2)):
        return sorted(result)

    return False

def is_satisfiable(clauses):
    while True:
        new_clauses = []

        for i in range(len(clauses) - 1):
            for j in range(i + 1, len(clauses)):
                new_clause = resolve_clauses(clauses[i], clauses[j])

                if new_clause == []:
                    return False
                elif new_clause and new_clause not in clauses and new_clause not in new_clauses:
                    new_clauses.append(new_clause)

        if new_clauses:
            clauses.extend(new_clauses)
        else:
            return True

start_time = time.time()

clauses = load_clauses(r"./clauses.cnf")
clauses = remove_trivial_clauses(clauses)

if is_satisfiable(clauses):
    print("The clauses are SATISFIABLE")
else:
    print("The clauses are UNSATISFIABLE")

process = psutil.Process(os.getpid())
memory = process.memory_info()
print(f"Memory used: {memory.rss}B")
print(f"Memory used: {memory.rss / 1024:.2f}KB")
print(f"Memory used: {memory.rss / (1024**2):.2f}MB")
print(f"Memory used: {memory.rss / (1024**3):.2f}GB")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Total execution time: {elapsed_time:.3f} seconds")
