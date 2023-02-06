# =============================
# Student Names: Somiona Tian
# Group ID: 20093560
# Date: 2-5-2022
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc: This file contains code for building different CSP models using three constraint
#       types: binary not-equal, n-ary all-different, and cage constraints.
#

# Look for #IMPLEMENT tags in this file.
"""
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

"""

from cspbase import *
from itertools import product, combinations, permutations


def binary_ne_grid(cagey_grid):
    """
    A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.
    """
    # Step 1: create domain for each variable
    n = cagey_grid[0]  # working with n*n grid
    domain = [i + 1 for i in range(n)]

    # Step 2: create variables
    var_array = [
        Variable(f"Cell({t[0]},{t[1]})", domain) for t in product(domain, domain)
    ]
    # Step 3: add constraints
    constraints = []

    # Constraints for rows
    """
    Binary not-equal constraints for rows means that each number from the same row should
    pairwise not be equal to each other. This is done by creating a constraint for each
    pair of variables in a row, and adding the satisfying tuples to the constraint.
    So there will be n choose 2 constraints for each row.
    Example: for a 3x3 grid, there will be 3 choose 2 = 3 constraints for each row.
    (C1, C2) (C1, C3) (C2, C3)
    """
    var_doms = [list(range(1, n + 1)), list(range(1, n + 1))]  # for satisfying tuples
    sat_tuples = [t for t in product(*var_doms) if t[0] != t[1]]

    for row in range(n):  # num of rows
        for pair in combinations(range(n), 2):
            cons = Constraint(
                f"Row{row + 1}({pair[0] + 1},{pair[1] + 1})",
                [var_array[row * n + pair[0]], var_array[row * n + pair[1]]],
            )
            # Step 4: add satisfying constraints
            cons.add_satisfying_tuples(sat_tuples)
            constraints.append(cons)

    # Constraints for columns (Similar to row)
    for col in range(n):  # num of rows
        for col_ele in combinations(range(n), 2):
            cons = Constraint(
                f"Col{col + 1}({col_ele[0] + 1}, {col_ele[1] + 1})",
                [var_array[col + col_ele[0] * n], var_array[col + col_ele[1] * n]],
            )
            # Step 4: add satisfying constraints
            cons.add_satisfying_tuples(sat_tuples)
            constraints.append(cons)

    # Step 5: return csp and var_array
    csp = CSP(f"{n}*{n}-BinaryGrid", var_array)
    for c in constraints:
        csp.add_constraint(c)
    return csp, var_array


def nary_ad_grid(cagey_grid):
    """
    A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.
    """
    # Step 1: create domain for each variable
    n = cagey_grid[0]  # working with n*n grid
    domain = [i + 1 for i in range(n)]

    # Step 2: create variables
    var_array = [
        Variable(f"Cell({t[0]},{t[1]})", domain) for t in product(domain, domain)
    ]
    # Step 3: add constraints
    constraints = []

    # Constraints for rows
    """
    We will create a constraint for each permutation of the variables in a row.
    Which means, n-ary all-different constraints applied for the n# of variables in a row.
    Example: for a 3x3 grid, there will be 3! = 6 constraints for each row.
    N-ary constraints: (C1,C2,C3) (C1,C3,C2) (C2,C1,C3) (C2,C3,C1) (C3,C1,C2) (C3,C2,C1)
    """
    sat_tuples = list(permutations(domain))

    for row in range(n):
        cons = Constraint(f"Row({row})", [var_array[row * n + var] for var in range(n)])
        # Step 4: add satisfying constraints
        cons.add_satisfying_tuples(sat_tuples)
        constraints.append(cons)

    # Constraints for columns (Similar to row)
    for col in range(n):
        cons = Constraint(f"Col({col})", [var_array[col + var * n] for var in range(n)])
        # Step 4: add satisfying constraints
        cons.add_satisfying_tuples(sat_tuples)
        constraints.append(cons)

    # Step 5: return csp and var_array
    csp = CSP(f"{n}*{n}-{n}aryGrid", var_array)
    for c in constraints:
        csp.add_constraint(c)
    return csp, var_array


def cagey_check(target, constraint):
    """
    takes a list of valuations and attempts to determine if this is a valid assignment
    Parameter:
        target (int): the target value
        operands (list): a list of integers with the last element being the operator
    Return True if target can be obtained by applying the operator to the operands
    """

    operator = constraint[-1]
    operands = constraint[:-1]
    try:
        if len(operands) == 1:
            return target == operands[0]
        elif len(operands) == 2:
            return target == eval(f"{operands[0]} {operator} {operands[1]}")
        else:
            value = operands[0]
            for i in range(1, len(operands)):
                value = eval(f"{value} {operator} {operands[i]}")
            return target == value
    except ZeroDivisionError:
        return False


def cagey_csp_model(cagey_grid):
    """
    A model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.

    Choose n-ary all-different constraints for the grid. My previous code generates
    less constraints than the binary not-equal constraints.

    Complain: Why test_cage_existence function just use string matching for finding the constraint?
              I mean, I need to adjust the variable naming strategy to make it work.
              And that was not in the scope of CSP logic.
    """
    # Step 1: create domain for each variable
    n = cagey_grid[0]  # working with n*n grid
    csp, var_arr = nary_ad_grid(cagey_grid)  # from n-ary function above

    # Consider Cagey cage
    for cage in cagey_grid[1]:
        target = cage[0]
        operator = cage[2]

        # Step 2: create variables
        valid_operators = ["+", "-", "*", "/"]
        cage_vars = [var_arr[(var[0] - 1) * n + (var[1] - 1)] for var in cage[1]]
        cage_constraint = Variable(f"Cage_op({target}:{operator}:{cage_vars})", valid_operators)

        # Step 3: add constraints
        csp.add_var(cage_constraint)
        constraints = cage_vars[:]
        constraints.append(cage_constraint)
        con = Constraint(f"Cage_op({target}:{operator}:{cage_vars})", constraints)

        # Add satisfying tuples based on the constraints
        cage_constraint.assign(operator)  # assign operator value as given

        var_domains = [v.cur_domain() for v in constraints]
        sat_tuples = []
        # Step 4: Test for any possible operator combinations.
        if (operator != "?") or (len(cage_vars) == 1):
            sat_tuples.extend(t for t in product(*var_domains) if cagey_check(target, t))
        else:  # Search for all the possible operator for ?
            for o in valid_operators:
                var_domains[-1] = o
                sat_tuples.extend(
                    t for t in product(*var_domains) if cagey_check(target, t)
                )
            # Step 4: add satisfying constraints
        con.add_satisfying_tuples(sat_tuples)
        # Add cage var and constraints to the csp Object
        var_arr.append(cage_constraint)
        csp.add_constraint(con)

    return csp, var_arr
