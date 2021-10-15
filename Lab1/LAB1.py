import math
import scipy.optimize
import numpy as np


def check_is_integer(list_x):
    res = True
    for xi in list_x:
        part = abs(xi - math.floor(xi))
        if 10**(-6) <= part <= 1 - 10**(-6):
            res = False
            break
    return res


def get_position_x(list_x):
    x_ind = 0
    for i, xi in enumerate(list_x):
        part = abs(xi - math.floor(xi))
        if 10**(-6) <= part <= 1 - 10**(-6):
            x_ind = i
            break
    return x_ind


def get_integer_part(x):
    if abs(math.floor(x + 1) - x) <= 10 ** (-6):
        return math.floor(x + 1)
    else:
        return math.floor(x)


def branch_and_bound_method(A, b, c, bounds, n):
    stack = [bounds]
    r = 0
    has_result = False
    opt_plan = np.zeros(range(n))
    while stack:
        print(f'stack = {stack}')
        current_bounds = stack.pop()
        print(f'current task = {current_bounds}')

        result = scipy.optimize.linprog(-c, A, b, bounds=current_bounds)
        current_opt_plan = result.x

        if result.success:
            print(f'current result = {current_opt_plan}')
            current_r = np.dot(c, current_opt_plan)
        else:
            print("The task is incompatible!")
            current_r = -np.Inf

        if not result.success or current_r <= r:
            if result.success:
                print('r* < r')
            print('Go to next iteration...')
            print('-------------------------------------------------')
            continue

        print(f'current r = {current_r}')
        is_int = check_is_integer(current_opt_plan)
        x_ind = get_position_x(current_opt_plan)
        int_r = get_integer_part(current_r)

        if is_int and int_r > r:
            opt_plan = current_opt_plan
            has_result = True
            r = int_r
            print(f'r = {r}')
            print(f'opt_plan = {opt_plan}')
            print('Go to next iteration...')
            print('-------------------------------------------------')
            continue

        x0 = current_opt_plan[x_ind]
        first_bound = math.floor(x0)
        second_bound = math.floor(x0 + 1)
        # print(first_bound)
        # print(second_bound)

        bounds1 = list(current_bounds)
        bounds1[x_ind] = [current_bounds[x_ind][0], first_bound]
        print(f'Add ILP: bound = {bounds1}, x_i = {x_ind}, first_bound = {first_bound}')

        bounds2 = list(current_bounds)
        bounds2[x_ind] = [second_bound, current_bounds[x_ind][1]]
        print(f'Add ILP: bound = {bounds2}, x_i = {x_ind}, second_bound = {second_bound}')

        stack.append(bounds2)
        stack.append(bounds1)
        print('-------------------------------------------------')

    return has_result, opt_plan


def main():
    A = np.array([[4, 3], [-4, 3]])
    n = 2
    b = np.array([22, 2])
    c = np.array([-5, 4])
    bounds = [[1, 4], [0, 5]]

    has_int_plans, opt_int_plan = branch_and_bound_method(A, b, c, bounds, n)

    if has_int_plans:
        print('Solution: x =', opt_int_plan)
    else:
        print('No solution found(')


if __name__ == "__main__":
    main()
