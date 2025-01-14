from z3 import *
from pprint import pprint

a = Int("a")
b = Int("b")

constraint = [a % b == 0]

s = Solver()
# s.add(digits_c)
s.add(constraint + [And(a >= 1, b >= 1)] + [a != b])

if s.check() == sat:
    m = s.model()
    # r = [[m.evaluate(X[i][j]) for j in range(9)] for i in range(9)]
    # print_matrix(r)
    # print(m.evaluate(excluded_digit))
    print(m.evaluate(a), m.evaluate(b))
    # print([m.evaluate(i) for i in digits])
else:
    print("failed to solve")


"""
The "digits" are 9 integer variables which are unique, and 0-9
Each row, column, square only contains unique digits
Evaluate the 9 digit number formed by each row
"""
