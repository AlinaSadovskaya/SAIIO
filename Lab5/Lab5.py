from collections import defaultdict
import numpy as np


def get_additional_graph(c, f, n):
    c_f = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            c_f[i][j] = c[i][j] - f[i][j]

    G_f = defaultdict(list)

    n, m = c_f.shape

    for i in range(n):
        for j in range(m):
            if c_f[i, j] > 0:
                G_f[i].append(j)

    return G_f, c_f


def tagging_method(G, start, end):
    visit = set()
    visit.add(start)
    Q = [start]
    l = {}

    while Q:
        u = Q.pop()
        for v in G[u]:
            if v not in visit:
                Q.append(v)
                visit.add(v)
                l[v] = u

    P = []
    if end in visit:
        P.append(end)
        while True:
            v = l[P[-1]]
            P.append(v)
            if v == start:
                break

    return P


def get_st_path(G_f, start, end):
    path = tagging_method(G_f, start, end)
    print('Path: ', path[::-1])
    P = []
    if path:
        for i in range(len(path) - 1):
            e = path[i]
            s = path[i + 1]
            P.append((s, e))

        P = P[::-1]
    return P


def ford_fulkerson(G, start, end, n):
    c = np.zeros((n, n))
    for uvm in G:
        c[uvm[0], uvm[1]] = uvm[2]
    n, m = c.shape
    f = np.zeros((n, m))
    max_flow = 0
    iter = 1
    while True:
        print('-----------------------------------')
        print('iter: ', iter)
        print('f: ', f)
        G_f, c_f = get_additional_graph(c, f, n)
        print('c_f: ', c_f)
        path = get_st_path(G_f, start, end)
        if not path:
            print('-----------------------------------')
            break
        theta = min([c_f[i, j] for i, j in path])
        print('theta: ', theta)
        max_flow += theta
        for u, v in path:
            f[u, v] += theta
            f[v, u] -= theta

        iter += 1

    # для красивого вывода
    G_res = defaultdict(list)
    for i in range(n):
        for j in range(n):
            if f[i, j] > 0:
                G_res[i].append(j)
            else:
                f[i, j] = 0
    return G_res, f, max_flow


if __name__ == '__main__':
    # n = 4
    # start, end = 0, 3
    #
    # G = [[0, 1, 3],
    #      [0, 2, 2],
    #      [1, 2, 2],
    #      [1, 3, 1],
    #      [2, 3, 2]]

    n = 6
    start, end = 0, 5

    G = [[0, 1, 7],
         [0, 3, 4],
         [1, 2, 2],
         [1, 3, 4],
         [2, 4, 4],
         [2, 5, 5],
         [3, 2, 8],
         [3, 4, 4],
         [4, 5, 12]]

    G_res, f, max_flow = ford_fulkerson(G, start, end, n)

    print('Поток с максимальной мощностью f: \n', f)
    # print('Граф G: \n', G_res)
    print('\nM(f): ', max_flow)
