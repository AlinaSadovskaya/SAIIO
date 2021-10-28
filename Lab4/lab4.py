import numpy as np
from collections import defaultdict


def create_graph(V_U):
    G = defaultdict(list)
    for uv in V_U:
        G[uv[0]].append(uv[1])
    return G


def depth_search(G, v, visited):
    visited.append(v)
    for v_i in G[v]:
        if v_i not in visited:
            depth_search(G, v_i, visited)


def topological_sort(G, v):
    visited = [v]
    for v_i in G[v]:
        if v_i not in visited:
            depth_search(G, v_i, visited)
    return visited


def create_path(V, prev, start, end):
    path = [end]
    index_prev = len(prev) - 1
    while True:
        node = prev[index_prev]
        path.append(node)
        if node == start:
            break
        index_prev = V.index(node)
    path.reverse()
    return path


def max_path(V_U, start, end):
    G = create_graph(V_U)
    sort_array = topological_sort(G, start)
    print('Топологическая сортировка: ', sort_array)

    if end not in sort_array:
        print(f'Вершина {start} недостижима из вершины {end}')
        return

    final_array = sort_array[:sort_array.index(end) + 1]
    print('Обрабатываемый массив вершин: ', final_array)

    final_V = []
    for v in V_U:
        if v[0] in final_array and v[1] in final_array:
            final_V.append(v)
    print('Обрабатываемый массив ребер: ', final_V)

    l = [0]
    prev = [-np.inf]

    for ind, elem in enumerate(final_array[1:]):
        max_value = -np.inf
        max_node = -np.inf
        print('-----------------')
        for v_i in [v_i for v_i in final_V if v_i[1] == elem]:
            temp_value = l[final_array.index(v_i[0])] + v_i[2]
            if max_value == -np.inf or temp_value > max_value:
                max_value = temp_value
                max_node = v_i[0]

        print('Step: ', ind+1)
        l.append(max_value)
        prev.append(max_node)
        print('l: ', l)
        print('prev: ', prev)

    print('-----------------')

    print('\nФинальный вектор l: ', l)
    print('Финальный вектор prev: ', prev)

    print('\nМаксимальный путь: ', l[-1])
    path = create_path(final_array, prev, start, end)
    print('Итоговый путь: ', path)


if __name__ == '__main__':
    V_U = [[1, 2, 1],
         [1, 4, 1],
         [2, 4, 2],
         [2, 3, 1],
         [3, 6, 1],
         [4, 5, 1],
         [5, 3, 2],
         [5, 6, 1],
         [7, 3, 3]]
    start = 1
    end = 6
    max_path(V_U, start, end)
