import sys

sys.stdin = open('input.txt')


def read_data_from_file():
    s, t = input().split()
    G = {}
    parents = {}
    while True:
        try:
            start_v, end_v, c = input().split()
        except EOFError:
            flag_check = 0
            for v in G:
                if t in G[v]:
                    flag_check += 1
            if s in G and flag_check > 0:
                break
            else:
                print('Вершина t не достижима из S')
                s = -1
                t = -1
                break
        else:
            if start_v in G:
                G[start_v][end_v] = float(c)
            else:
                G[start_v] = {end_v: float(c)}
            parents[end_v] = None

    return G, parents, s, t


def min_cost_node(costs, Q):
    min_cost = float('inf')
    node = None

    for v in costs:
        curent_cost = costs[v]
        if curent_cost < min_cost and v not in Q:
            min_cost = curent_cost
            node = v

    return node


def dijkstra(G, parents, s, t):
    costs = {}
    for node in parents:
        costs[node] = float('inf')

    for child in G[s]:
        parents[child] = s
        costs[child] = G[s][child]

    G[t] = {}
    Q = []

    while True:
        node = min_cost_node(costs, Q)
        if node is None:
            break

        cost = costs[node]
        if node in G:
            childs = G[node]
            for child in childs:
                new_cost = cost + childs[child]
                if costs[child] > new_cost:
                    costs[child] = new_cost
                    parents[child] = node
            Q.append(node)
        else:
            Q.append(node)

    final_cost = costs[t]
    path = []
    next_node = t
    while True:
        path.append(next_node)
        if next_node == s:
            break
        else:
            next_node = parents[next_node]

    return final_cost, path


if __name__ == "__main__":
    G, parents, s, t = read_data_from_file()
    if t != -1 and s != -1:
        res_cost, res_path = dijkstra(G, parents, s, t)
        print('Min path:', res_cost)
        for i in range(len(res_path)):
            if i != len(res_path) - 1:
                print(res_path[len(res_path) - i - 1], end='->')
            else:
                print(res_path[len(res_path) - i - 1], end='')
