import math
import os
import random
import re
import sys
from functools import cache
from itertools import combinations


def cache_solve(h, target, queries):
    """Lookup or compute & store technique."""

    @cache
    def _helper(a, b, target):
        return abs(h[a] - h[b]) <= target

    combos = (combinations(range(j,k+1), 2) for j, k in queries)
    return [sum(_helper(a, b, target) for a, b in pairs) for pairs in combos]


def solve(h, target, queries):
    """Determine all valid pairs amongst those in the queries."""
    pairs = {pair for j, k in queries for pair in combinations(range(j,k+1), 2)}
    valid_pairs = {(a, b,) for a, b in pairs if abs(h[a] - h[b]) <= target}
    q_combos = (combinations(range(j,k+1), 2) for j, k in queries)
    return [sum(pair in valid_pairs for pair in q_pairs) for q_pairs in q_combos]



if __name__ == '__main__':
    first_multiple_input = input().rstrip().split()
    n = int(first_multiple_input[0])
    k = int(first_multiple_input[1])
    h = list(map(int, input().rstrip().split()))
    q = int(input().strip())
    queries = []
    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))
    result = solve(h, k, queries)
    output = '\n'.join(map(str, result))
    print(output)
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    # fptr.write(output)
    # fptr.write('\n')
    # fptr.close()
