from z3 import *
from pprint import pprint

POW = [1e8, 1e7, 1e6, 1e5, 1e4, 1e3, 1e2, 1e1, 1e0]
POW = [int(i) for i in POW]


# First we create an Integer Variable for each cell of the Sudoku grid.
X = [[Int("x_%s_%s" % (i + 1, j + 1)) for j in range(9)] for i in range(9)]
excluded_digit = Int("excluded")

# digits = [Int("digit_%s") % i for i in range(9)]
# Each digit must be unique
# digits_c = [Distinct(digits)]
# Each digit must be between 0 and 9 inclusive
# digits_c += [And(0 <= i, i <= 9) for i in digits]


excluded_digit_c = [And(0 <= excluded_digit, excluded_digit <= 9)]
# Each cell must contain a digit (1 to 9)
cells_c = [And(0 <= X[i][j], X[i][j] <= 9) for i in range(9) for j in range(9)]

# Every digit has to be placed exactly once in each row
rows_c = [Distinct(X[i] + [excluded_digit]) for i in range(9)]

# Every digit has to be placed exactly once in each column

cols_c = [Distinct([X[i][j] for i in range(9)] + [excluded_digit]) for j in range(9)]
# Every digit has to be placed exactly once in each 3x3 subgrid

sq_c = [
    Distinct(
        [X[3 * i0 + i][3 * j0 + j] for i in range(3) for j in range(3)]
        + [excluded_digit]
    )
    for i0 in range(3)
    for j0 in range(3)
]
# # Now that we have each condition as code, we can chain these conditions:


# def create_number(divisor, num_list, var_name):
#     num = 0
#     for ind, val in enumerate(num_list):
#         num += val * POW[ind]
#     return num % divisor == 0


def create_number(number_var, num_list):
    # TODO
    num = 0
    for ind, val in enumerate(num_list):
        num += val * POW[ind]
    return number_var == num


divisor = Int("divisor")
numbers = [Int(f"num_{i}") for i in range(9)]
# Each constructed number is equal to the dot product of its row
numbers_dot_c = [create_number(numbers[ind], row) for ind, row in enumerate(X)]
# Each number is divisible by the divisor
numbers_div_c = [number % divisor == 0 for number in numbers]

# numbers_c = [create_number(divisor, row, f"num_{ind}") for ind, row in enumerate(X)]

sudoku_c = (
    excluded_digit_c + cells_c + rows_c + cols_c + sq_c + numbers_dot_c + numbers_div_c
)

# instance = (
#     (5, 3, 0, 0, 7, 0, 0, 0, 0),
#     (6, 0, 0, 1, 9, 5, 0, 0, 0),
#     (0, 9, 8, 0, 0, 0, 0, 6, 0),
#     (8, 0, 0, 0, 6, 0, 0, 0, 3),
#     (4, 0, 0, 8, 0, 3, 0, 0, 1),
#     (7, 0, 0, 0, 2, 0, 0, 0, 6),
#     (0, 6, 0, 0, 0, 0, 2, 8, 0),
#     (0, 0, 0, 4, 1, 9, 0, 0, 5),
#     (0, 0, 0, 0, 8, 0, 0, 7, 9),
# )

instance = (
    (-1, -1, -1, -1, -1, -1, -1, 2, -1),
    (-1, -1, -1, -1, -1, -1, -1, -1, 5),
    (-1, 2, -1, -1, -1, -1, -1, -1, -1),
    (-1, -1, 0, -1, -1, -1, -1, -1, -1),
    (-1, -1, -1, -1, -1, -1, -1, -1, -1),
    (-1, -1, -1, 2, -1, -1, -1, -1, -1),
    (-1, -1, -1, -1, 0, -1, -1, -1, -1),
    (-1, -1, -1, -1, -1, 2, -1, -1, -1),
    (-1, -1, -1, -1, -1, -1, 5, -1, -1),
)

# print_matrix(instance)

instance_c = [
    If(instance[i][j] == -1, True, X[i][j] == instance[i][j])
    for i in range(9)
    for j in range(9)
]

s = Optimize()
s.add(sudoku_c + instance_c)
s.maximize(divisor)

if s.check() == sat:
    m = s.model()
    r = [[m.evaluate(X[i][j]) for j in range(9)] for i in range(9)]
    print_matrix(r)
    print(m.evaluate(excluded_digit))
    # print([m.evaluate(i) for i in digits])
    for n in numbers:
        print(m.evaluate(n))
    print(m.evaluate(divisor))
else:
    print("failed to solve")


"""
The "digits" are 9 integer variables which are unique, and 0-9
Each row, column, square only contains unique digits
Evaluate the 9 digit number formed by each row
"""
