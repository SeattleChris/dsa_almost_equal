# import os
from collections import defaultdict
from functools import cache
from itertools import chain, combinations


def cache_solve(h, target, queries):
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


def find_valid_combo_solve(h, target, queries):
    """4min 33sec. Determine all valid pairs amongst those in the queries."""
    pairs = {pair for j, k in queries for pair in combinations(range(j,k+1), 2)}
    valid_pairs = {(a, b,) for a, b in pairs if abs(h[a] - h[b]) <= target}
    q_combos = (combinations(range(j,k+1), 2) for j, k in queries)
    return [sum(pair in valid_pairs for pair in q_pairs) for q_pairs in q_combos]


def cache_seq_solve(h, target, queries):
    """2min 44sec. Using sequence for pairing and cache of pair results."""
    @cache
    def _helper(j, k):
        return abs(h[j] - h[k]) <= target

    return [sum(_helper(j, k) for j in range(a, b) for k in range(j + 1, b + 1)) for a, b in queries]


def seq_set_solve(h, target, queries):
    """2min 3sec. Sets of valid paired indexes."""
    paired = [set() for _ in h]  # all indices that will be paired with a given index
    for a, b in queries:
        for j in range(a, b):
            paired[j].update(range(j+1, b+1))
    valid = [
        {idx for idx in group if abs(h[pos] - h[idx]) <= target}
        for pos, group in enumerate(paired)
        ]
    return [sum(j in valid[i] for i in range(a, b) for j in range(i + 1, b + 1)) for a, b in queries]


def valid_pair_solve(h, target, queries):
    """3min 6sec (combinations 3min 11sec). Sets of valid paired indexes."""
    paired = [set() for _ in h]  # all indices that will be paired with a given index
    for a, b in queries:
        for j in range(a, b):
            paired[j].update(range(j+1, b+1))
    valid = {
        (pos, idx)
        for pos, group in enumerate(paired)
        for idx in group
        if abs(h[pos] - h[idx]) <= target
        }
    return [
        sum(
            (i, j) in valid
            for i in range(a, b)
            for j in range(i + 1, b + 1)
            )
        for a, b in queries
        ]


def setdefault_solve(h, target, queries):
    """2min 36sec. Use Dict.setdefault of paired indexes."""
    matrix = [dict() for _ in h]
    results = []
    for a, b in queries:
        score = 0
        for j in range(a, b):
            for k in range(j+1, b+1):
                score += matrix[j].setdefault(k, abs(h[j] - h[k]) <= target)
        results.append(score)
    return results


def fly2_solve(h, target, queries):
    """2min 1sec. On the fly determine if already known or compute value."""
    matrix = [[-1] * len(h) for _ in h]
    results = []
    for a, b in queries:
        score = 0
        for j in range(a, b):
            for k in range(j+1, b+1):
                matrix[j][k] = (res := matrix[j][k] if matrix[j][k] != -1 else abs(h[j] - h[k]) <= target)
                score += res
        results.append(score)
    return results


def matrix_chain_solve(h, target, queries):
    """1min 46sec. Matrix of paired indexes."""
    matrix = [[0] * len(h) for _ in h]
    paired = [[] for _ in h]  # all indices that will be paired with a given index
    for a, b in queries:
        for j in range(a, b):
            paired[j].append(range(j+1, b+1))  # += [x for x in range(j +1, b+1)]
    for pos, group in enumerate(paired):
        for idx in set(chain.from_iterable(group)):
            matrix[pos][idx] = abs(h[pos] - h[idx]) <= target
    return [sum(matrix[i][j] for i in range(a, b) for j in range(i + 1, b + 1)) for a, b in queries]


def fly_no_save_solve(h, target, queries):
    """1min 55sec, 2min 48sec with cache helper. Matrix of paired indexes."""
    results = []
    for a, b in queries:
        score = 0
        for pos in range(a, b):
            for idx in range(pos+1, b+1):
                score += abs(h[pos] - h[idx]) <= target
        results.append(score)
    return results


def fly_cache_solve(h, target, queries):
    """2min 45sec. On the fly with cache for value."""
    @cache
    def _helper(j, k):
        return abs(h[j] - h[k]) <= target

    return [
        sum(
            _helper(j, k)
            for j in range(a, b)
            for k in range(j+1, b+1)
            )
        for a, b in queries
        ]


def matrix_set_solve(h, target, queries):
    """1min 37sec. Matrix of paired indexes."""
    matrix = [[0] * len(h) for _ in h]
    paired = [set() for _ in h]  # all indices that will be paired with a given index
    for a, b in queries:
        for j in range(a, b):
            paired[j].update(range(j+1, b+1))
    for pos, group in enumerate(paired):
        for idx in group:
            matrix[pos][idx] = abs(h[pos] - h[idx]) <= target
    return [sum(matrix[i][j] for i in range(a, b) for j in range(i + 1, b + 1)) for a, b in queries]


def fly_solve(h, target, queries):
    """1min 29sec (16s lookup, 46s if-else, 25s no save) On the fly per query."""
    matrix = [[-1] * len(h) for _ in h]
    results = []
    for a, b in queries:
        score = 0
        for j in range(a, b):
            for k in range(j+1, b+1):
                if (res := matrix[j][k]) == -1:
                    matrix[j][k] = (res := abs(h[j] - h[k]) <= target)
                score += res
        results.append(score)
    return results


def match_solve(h, target, queries):
    """4min 45sec. Collect all pairs to compute along with query source."""
    matrix = [[0] * len(h) for _ in h]
    source = [defaultdict(list) for _ in h]  # query sources for a given pair
    paired = [set() for _ in h]  # all indices that will be paired with a given index
    results = [0 for _ in queries]
    for num, (a, b) in enumerate(queries):
        for j in range(a, b):
            paired[j].update(range(j+1, b+1))
            # source[j]
            for idx in range(j+1, b+1):
                source[j][idx].append(num)
    for pos, group in enumerate(paired):
        for idx in group:
            if abs(h[pos] - h[idx]) <= target:
                matrix[pos][idx] = 1
                for query in source[pos][idx]:
                    results[query] += 1
    return results


def solve(h, target, queries):
    return fly_solve(h, target, queries)


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
