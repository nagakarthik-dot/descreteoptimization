#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def knapSack(W, wt, val, n):
    # Making the dp array
    dp = [0 for _ in range(W + 1)]
    keep = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Fill dp array and keep track of items included
    for i in range(1, n + 1):
        for w in range(W, 0, -1):
            if wt[i - 1] <= w:
                if dp[w] < dp[w - wt[i - 1]] + val[i - 1]:
                    dp[w] = dp[w - wt[i - 1]] + val[i - 1]
                    keep[i][w] = 1
                else:
                    keep[i][w] = 0

    # Find out which items to take
    w = W
    taken = [0] * n
    for i in range(n, 0, -1):
        if keep[i][w] == 1:
            taken[i - 1] = 1
            w -= wt[i - 1]

    return dp[W], taken

def solve_it(input_data):
    # Parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    values = []
    weights = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    # Solve the knapsack problem
    max_value, taken = knapSack(capacity, weights, values, item_count)

    # Prepare the solution in the specified output format
    output_data = str(max_value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data





if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

