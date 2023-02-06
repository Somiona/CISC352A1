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

#Look for #IMPLEMENT tags in this file.
'''
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

'''

from cspbase import *
from itertools import product, combinations, permutations

def binary_ne_grid(cagey_grid):
    """
    A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.
    """
    # Step 1: create domain for each variable
    n = cagey_grid[0] # working with n*n grid
    domain = [i + 1 for i in range(n)]

    # Step 2: create variables
    var_array = [
        Variable(f'({t[0]},{t[1]})', domain) for t in product(domain, domain)
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
    var_doms = [list(range(1, n+1)),list(range(1, n+1))] # for satisfying tuples
    sat_tuples = [t for t in product(*var_doms) if t[0] != t[1]]

    for row in range(n): # num of rows
        for pair in combinations(range(n), 2):
            cons = Constraint(f"C(Row{row + 1}({pair[0] + 1},{pair[1] + 1})",
                             [var_array[row * n + pair[0]],var_array[row * n + pair[1]]])
            # Step 4: add satisfying constraints
            cons.add_satisfying_tuples(sat_tuples)
            constraints.append(cons)

    # Constraints for columns (Similar to row)
    for col in range(n): # num of rows
        for pair in combinations(range(n), 2):
            cons = Constraint(f"C(Col{col+1}({pair[0]+1},{pair[1]+1})",
                              [var_array[col+pair[0]*n],var_array[col+pair[1]*n]])
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
    n = cagey_grid[0] # working with n*n grid
    domain = [i+1 for i in range(n)]

    # Step 2: create variables
    var_array = [Variable(f'Cell({t[0]},{t[1]})', domain) for t in product(domain,domain)]
    # Step 3: add constraints
    constraints = []

    # Constraints for rows
    """
    We will create a constraint for each permutation of the variables in a row.
    Which means, n-ary all-different constraints applied for the n# of variables in a row.
    Example: for a 3x3 grid, there will be 3! = 6 constraints for each row.
    N-ary constraints: (C1,C2,C3) (C1,C3,C2) (C2,C1,C3) (C2,C3,C1) (C3,C1,C2) (C3,C2,C1)
    """
    all_possible = list(combinations(domain, n))

    for row in range(n):
        for t in combinations(range(n), n):
            cons = Constraint(f"C(Row{row + 1}-{t})", [var_array[row * n + var] for var in t])
            # Step 4: add satisfying constraints
            cons.add_satisfying_tuples(all_possible)
            constraints.append(cons)

    # Constraints for columns (Similar to row)
    for col in range(n):
        for t in combinations(range(n), n):
            cons = Constraint(f"C(Col{col + 1}-{t})", [var_array[col+var*n] for var in t])
            # Step 4: add satisfying constraints
            cons.add_satisfying_tuples(all_possible)
            constraints.append(cons)

    # Step 5: return csp and var_array
    csp = CSP(f"{n}*{n}-{n}aryGrid", var_array)
    for c in constraints:
        csp.add_constraint(c)
    return csp, var_array


def coord_to_index(coordinate, n):
    """
    Transform Coordinate to index position
    T(x,y) --> i  (n is size of grid/matrix)
    T(x,y) = (x-1) * n + (y-1)
    """
    x, y = coordinate[0], coordinate[1]
    return (x - 1) * n + (y - 1)

def evaluate(op1, op2, operator):
    """
    Evaluate the math statement op1 operator op2
    Return an integer value
    """
    if operator == "+":
        return op1 + op2
    elif operator == "-":
        return op1 - op2
    elif operator == "*":
        return op1 * op2
    elif operator == "/":
        return op1 / op2

def cagey_check(target, operands):
    """
    takes a list of valuations and attempts to determine if this is a valid assignment
    :parm target (natural num), operands (a list of integers with an operator in the last index)
    Return True/False
    """
    value = 0
    operator = operands[-1]
    operands = operands[:-1]
    if len(operands) == 1:
        return target == operands[0]
    elif len(operands) == 2:
        return target == abs(evaluate(operands[0],operands[1],operator))
    else:
        value = operands[0]
        for i in range(1,len(operands)):
            value = evaluate(value, operands[i], operator)
        return target == abs(value)

# Testing cases
##print("6, [1,2,3], '+' is ", cagey_check(6, [1,2,3], '+'))
##print("6, [1,2,3], '-' is ", cagey_check(6, [1,2,3], '-'))
##print("108, [6,3,6], '*' is ", cagey_check(108, [6,3,6], '*'))
##print("1, [6,5], '-' is ", cagey_check(1, [6,5], '-'))
##print("1, [5,6], '-' is ", cagey_check(1, [5,6], '-'))
##print("4, [16,2,2], '/' is ", cagey_check(4, [16,2,2], '/'))

def cagey_csp_model(cagey_grid):
    """
    Desc: a model of a Cagey grid built using choice (1) binary not-equal
          constraints for the grid, together with Cagey cage constraints.

    Reason: for faster computation in terms of number of constraints
        For n x n grid
            num of binary constraints
            (row + col) n x nC2 + n x nC2 = 2n x nC2

            num of n-ary constraints
            (row + col) n x n! + n x n! = 2n x n!
        which means num of binary < num of n-ary constraints
    """
    n = cagey_grid[0] # n x n grid
    #csp, var_arr = nary_ad_grid((cagey_grid[0],[])) # from n-ary function above
    csp, var_arr = binary_ne_grid((cagey_grid[0],[])) # from binary function above

    # Consider Cagey cage
    for count, cage in enumerate(cagey_grid[1]):
        target = cage[0]
        operator = cage[2]
        in_cage = []

        # Add cage constraint & cage variable
        dom = ["+","-","*","/","?"]

        for var in cage[1]: # convert coordinate to index and include into constraint
            in_cage.append(var_arr[coord_to_index(var, n)])
        cage_oper = Variable(f'Cage_op({target}:{operator}:{in_cage})', dom)

        # Add cage variable to csp
        csp.add_var(cage_oper)
        varlist = in_cage[:]
        varlist.append(cage_oper)
        con = Constraint(f'Cage_op({target}:{operator}:{in_cage})', varlist)

        # Add satisfying tuples based on the constraints
        cage_oper.assign(operator) # assign operator value as given

        varDoms = []
        for v in varlist:
            varDoms.append(v.cur_domain()) # since we select specific operator

        sat_tuples = []
        if (operator != "?") or (len(in_cage) == 1):
            for t in product(*varDoms):
                if cagey_check(target, t):
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
        else: # which mean it is ?
            trys = ["+","-","*","/"]
            for oper in trys:
                varDoms[-1] = oper
                for t in product(*varDoms):
                    if cagey_check(target, t):
                        sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)

        # Add cage var and constraints to the csp Object
        var_arr.append(cage_oper)
        csp.add_constraint(con)

    return csp, var_arr

# Testing cases
##binary = binary_ne_grid((3,[])) # without cage constraints
##n_ary = nary_ad_grid((3,[]))    # without cage constraints
##a, b = cagey_csp_model((3, [(3,[(1,1), (2,1)],'+'),
##                    (1, [(1,2)], '?'),
##                    (8, [(1,3), (2,3), (2,2)], "+"),
##                    (3, [(3,1)], '?'),
##                    (3, [(3,2), (3,3)], "+")]
##                )
##               )
##print(b)

##for key, val in a.vars_to_cons.items():
##    val_name = []
##    for i in val:
##        val_name.append(i.name)
##    print(key,val_name)
