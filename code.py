# import os
from functools import cache
from itertools import combinations


def solve(h, target, queries):
    """3min 8sec. Lookup or compute & cache technique."""

    @cache
    def _helper(a, b):
        return abs(h[a] - h[b]) <= target

    combos = (combinations(range(j,k+1), 2) for j, k in queries)
    return [sum(_helper(a, b) for a, b in pairs) for pairs in combos]


def stored_solve(h, target, queries):
    """3min 57sec. Lookup or compute & store technique."""
    data = {}
    combos = (combinations(range(j,k+1), 2) for j, k in queries)
    return [sum(data.setdefault((a, b), abs(h[a] - h[b]) <= target) for a, b in pairs) for pairs in combos]



def find_valid_solve(h, target, queries):
    """4min 33sec. Determine all valid pairs amongst those in the queries."""
    pairs = {pair for j, k in queries for pair in combinations(range(j,k+1), 2)}
    valid_pairs = {(a, b,) for a, b in pairs if abs(h[a] - h[b]) <= target}
    q_combos = (combinations(range(j,k+1), 2) for j, k in queries)
    return [sum(pair in valid_pairs for pair in q_pairs) for q_pairs in q_combos]



if __name__ == '__main__':
    first_multiple_input = input().rstrip().split()
    n = int(first_multiple_input[0])
    target = int(first_multiple_input[1])
    h = list(map(int, input().rstrip().split()))
    q = int(input().strip())
    queries = []
    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))
    result = solve(h, target, queries)
    output = '\n'.join(map(str, result))
    print(output)
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    # fptr.write(output)
    # fptr.write('\n')
    # fptr.close()
