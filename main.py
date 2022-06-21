# https://www.geeksforgeeks.org/2-satisfiability-2-sat-problem/
# https://cp-algorithms.com/graph/2SAT.html

from collections import defaultdict


def read_2sat(path):
    var1 = []
    var2 = []
    with open(path, 'r') as file:
        line = file.readline()
        n, clauses_count = line.split()
        for line in file:
            clause = line.split()
            var1.append(int(clause[0]))
            var2.append(int(clause[0]) if len(clause) == 2 else int(clause[1]))

    return int(n), int(clauses_count), var1, var2


def dfs_first(u, visited, adj, stack):
    if visited[u]:
        return

    visited[u] = True

    for i in adj[u]:
        dfs_first(i, visited, adj, stack)

    stack.append(u)


def dfs_second(u, visited_inv, adj_inv, scc, counter):
    if visited_inv[u]:
        return

    visited_inv[u] = True

    for i in adj_inv[u]:
        dfs_second(i, visited_inv, adj_inv, scc, counter)

    scc[u] = counter


def is2_satisfiable():
    n, clauses_count, var1, var2 = read_2sat('input.txt')
    adj = defaultdict(set)
    adj_inv = defaultdict(set)

    for i in range(clauses_count):

        if var1[i] > 0 < var2[i]:
            adj[var1[i] + n].add(var2[i])
            adj_inv[var2[i]].add(var1[i] + n)
            adj[var2[i] + n].add(var1[i])
            adj_inv[var1[i]].add(var2[i] + n)

        elif var1[i] > 0 and var2[i] < 0:
            adj[var1[i] + n].add(n - var2[i])
            adj_inv[n - var2[i]].add(var1[i] + n)
            adj[-var2[i]].add(var1[i])
            adj_inv[var1[i]].add(-var2[i])

        elif var1[i] < 0 and var2[i] > 0:
            adj[-var1[i]].add(var2[i])
            adj_inv[var2[i]].add(-var1[i])
            adj[var2[i] + n].add(n - var1[i])
            adj_inv[n - var1[i]].add(var2[i] + n)

        else:
            adj[-var1[i]].add(n - var2[i])
            adj_inv[n - var2[i]].add(-var1[i])
            adj[-var2[i]].add(n - var1[i])
            adj_inv[n - var1[i]].add(-var2[i])

    visited = defaultdict(bool)
    visited_inv = defaultdict(bool)

    stack = []
    for i in range(1, 2 * n + 1):
        if not visited_inv[i]:
            dfs_first(i, visited, adj, stack)

    counter = 0
    scc = dict()
    while stack:
        top = stack.pop()
        if not visited_inv[top]:
            dfs_second(top, visited_inv, adj_inv, scc, counter)
            counter += 1

    result = []
    for i in range(1, n + 1):
        if scc[i] == scc[i + n]:
            return
        result.append('PRAVDA' if scc[i] > scc[i + n] else 'NEPRAVDA')

    return result


def print_result(result):
    if result:
        print("SPLNITEĽNÁ")
        for i, item in enumerate(result):
            print(i + 1, item)
    else:
        print("NESPLNITEĽNÁ")


def main():
    result = is2_satisfiable()
    print_result(result)


if __name__ == "__main__":
    main()
