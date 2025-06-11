from collections import defaultdict
from typing import List

def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
    """
    Tarjan’s O(V+E) bridge-finding algorithm.
    Returns every edge whose removal disconnects the graph.
    """
    adj = defaultdict(list)
    for u, v in connections:          # build adjacency list
        adj[u].append(v)
        adj[v].append(u)

    disc = [-1] * n                   # discovery time of each node
    low  = [0]  * n                   # lowest discovery time reachable
    time = 0                          # global DFS timer
    bridges = []                      # answer list

    def dfs(u: int, parent: int) -> None:
        nonlocal time
        disc[u] = low[u] = time       # timestamp current node
        time += 1

        for v in adj[u]:
            if v == parent:           # skip the edge back to parent
                continue
            if disc[v] == -1:         # tree edge
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:  # bridge condition
                    bridges.append([u, v])
            else:                     # back edge
                low[u] = min(low[u], disc[v])

    for i in range(n):                # handle any components just in case
        if disc[i] == -1:
            dfs(i, -1)

    return bridges