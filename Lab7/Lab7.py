def basis_graph(n, G):
    g = dict()
    for v in range(n):
        g[v] = []

    for i in range(n):
        for j in range(len(G)):
            if G[j][4] == 1:
                if i == G[j][0]:
                    g[i].append(G[j][1])
                    g[G[j][1]].append(i)
    return g


def get_u(v, gb, G, u, is_visited):
    is_visited[v] = True
    for to in gb[v]:
        if not is_visited[to]:
            for elem in G:
                if v == elem[0] and to == elem[1]:
                    u[to] = u[v] - elem[2]
                elif v == elem[1] and to == elem[0]:
                    u[to] = u[v] + elem[2]
            get_u(to, gb, G, u, is_visited)


def find_u(n, gb, G):
    is_visited = [False for i in range(n)]
    u = [0 for i in range(n)]
    u[0] = 0
    get_u(0, gb, G, u, is_visited)
    return u


def find_uncorrect_condition(G, u):
    delta = []
    for elem in G:
        if elem[4] == 0:
            delta.append(((elem[0], elem[1]), u[elem[0]] - u[elem[1]] - elem[2]))

    delta_list = [elem[1] for elem in delta]
    return delta, delta_list


def remove_edge(G, n, new_edge):
    temp_gb = basis_graph(n, G)
    cycle = get_cycle(new_edge[0], n, temp_gb)
    U_plus = []
    U_minus = []
    for i in range(len(cycle) - 1):
        for elem in G:
            if cycle[i] == elem[0] and cycle[i + 1] == elem[1]:
                U_plus.append((cycle[i], cycle[i + 1]))
                break
            elif cycle[i] == elem[1] and cycle[i + 1] == elem[0]:
                U_minus.append((cycle[i + 1], cycle[i]))
                break

    if new_edge not in U_plus:
        U_minus, U_plus = U_plus[:], U_minus[:]

    tetta = []
    for elem in G:
        tupl = (elem[0], elem[1])
        if tupl in U_minus:
            tetta.append((tupl, elem[3]))

    # print('tetta: ', tetta)

    tetta_min = min([tetta[i][1] for i in range(len(tetta))])
    print('tetta : ', tetta_min)
    for elem in tetta:
        if elem[1] == tetta_min:
            remove_edge = elem[0]
            break

    for curve in U_plus:
        for i in range(len(G)):
            if curve[0] == G[i][0] and curve[1] == G[i][1]:
                G[i][3] += tetta_min
                break

    for curve in U_minus:
        for i in range(len(G)):
            if curve[0] == G[i][0] and curve[1] == G[i][1]:
                G[i][3] -= tetta_min
                break
    print('Удаляем дугу: (', remove_edge[0]+1, ',', remove_edge[1]+1, ')')
    for i in range(len(G)):
        if remove_edge[0] == G[i][0] and remove_edge[1] == G[i][1]:
            G[i][4] = 0
            break

    return G


def find_cycle(v, is_visited, p, g, cycle_st, cycle_end):
    is_visited[v] = 1
    cycle_st_new = cycle_st
    cycle_end_new = cycle_end
    for to in g[v]:
        if is_visited[to] == 0:
            p[to] = v
            flag, cycle_st_new, cycle_end_new = find_cycle(to, is_visited, p, g, cycle_st_new, cycle_end_new)
            if flag:
                return True, cycle_st_new, cycle_end_new

        elif (is_visited[to] == 1) and (p[v] != to):
            cycle_end_new = v
            cycle_st_new = to
            return True, cycle_st_new, cycle_end_new

    is_visited[v] = 2
    return False, cycle_st, cycle_end


def get_cycle(uu, n, g):
    is_visited = []
    p = []
    for i in range(n):
        is_visited.append(0)
        p.append(-1)

    flag, cycle_start, cycle_end = find_cycle(uu, is_visited, p, g, -1, -n-1)
    if flag:
        temp_cycle = []
        v = cycle_end
        while v != cycle_start:
            temp_cycle.append(v)
            v = p[v]

        temp_cycle.append(cycle_start)
        temp_cycle.reverse()
        temp_cycle.append(temp_cycle[0])

        return temp_cycle


def find_min_cost_path(n, G):
    iter = 1
    while True:
        print('---------------------------------------')
        print('iter = ', iter)
        print('---------------------------------------')
        gb = basis_graph(n, G)
        u = find_u(n, gb, G)
        for i, ui in enumerate(u):
            print('u', i+1, ' = ', ui)
        delta, delta_list = find_uncorrect_condition(G, u)
        max_delta = max(delta_list)
        if max_delta <= 0:
            print('Решение найдено!')
            # sum = 0
            # for elem in G:
            #     sum += elem[2] * elem[3]
            # print(sum)
            return G

        ind = delta_list.index(max_delta)
        new_edge = delta[ind][0]
        print('Добавили дугу: (', new_edge[0]+1, ',', new_edge[1]+1, ')')
        for i in range(len(G)):
            if G[i][0] == new_edge[0] and G[i][1] == new_edge[1]:
                G[i][4] = 1

        G = remove_edge(G, n, new_edge)

        print('Поток выглядит следующим образом:')
        iter += 1
        for i in G:
            if i[3] != 0:
                print(i[0] + 1, " -> ", i[1] + 1, " : ", i[3])

        print()


if __name__ == "__main__":
    G = [
        [0, 1, 1, 1, 1],
        [1, 5, 3, 0, 0],
        [2, 1, 3, 3, 1],
        [2, 3, 5, 1, 1],
        [4, 2, 4, 0, 0],
        [4, 3, 1, 5, 1],
        [5, 0, -2, 0, 0],
        [5, 2, 3, 9, 1],
        [5, 4, 4, 0, 0]
    ]
    n = 6
    res = find_min_cost_path(n, G)
    for i in res:
        if i[3] != 0:
            print(i[0] + 1, " -> ", i[1] + 1, " : ", i[3])
