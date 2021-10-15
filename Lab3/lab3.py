def solve(A, q, n):
    OPT = []
    X = []

    for i in range(0, q):
        opt_i = []
        x_i = []
        if i == 0:
            opt_i = A[0]
            x_i = A[0]
        else:
            for y in range(0, n):
                q_i = []
                for z in range(0, y + 1):
                    q_i.append(A[i][z] + OPT[i - 1][y - z])
                if not q_i:
                    opt_i.append(0)
                else:
                    # print('q_i = ', q_i)
                    max_opt = max(q_i)
                    max_index = q_i.index(max_opt)
                    opt_i.append(max_opt)
                    x_i.append(max_index)
        print('k = ', i + 1)
        print(f'X[{i}] = ', x_i)
        print(f'OPT[{i}] = ', opt_i)
        OPT.append(opt_i)
        X.append(x_i)
    return OPT, X


def find_opt_resources(n, q, OPT, X):
    res = q
    x_result = {}
    for z in range(n):
        max_profit_row = max(OPT)
        # print('max_profit_row = ', max_profit_row)
        max_profit = max(max_profit_row)
        # print('max_profit = ', max_profit)
        row = OPT.index(max_profit_row)
        column = OPT[row].index(max_profit)
        # print('row_i = ', row)
        # print('column_i = ', column)
        res_for_max = X[row][column]
        res = res - res_for_max
        x_result[row] = res_for_max
        OPT[row] = [-1] * q
        for i in range(0, n):
            for j in range(res, q):
                OPT[i][j] = -1
        # print(OPT)
    return x_result


if __name__ == "__main__":
    A = [[0, 1, 2, 3], [0, 0, 1, 2], [0, 2, 2, 3]]
    print('A = ', A)
    q = len(A[0])
    print('q = ', q - 1)
    n = len(A)
    print('n = ', n)
    print('------------------------------')
    OPT, X = solve(A, n, q)
    print('\nOPT: ', OPT)
    print('X: ', X)
    x = find_opt_resources(n, q, OPT, X)
    print('\nres = ', x)
