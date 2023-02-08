# =============================
# Student Names: Jingyi Cheng
# Group ID: 23
# Date:
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic '''
    maxLen = -1
    vars = csp.get_all_unasgn_vars()
    largest = None
    # get list of all unassigned variables loop through
    for var in vars:
        # list of constraints that include var in their scope
        cons = csp.get_cons_with_var(var)
        if len(cons) > maxLen:
            maxLen = len(cons)
            largest = var
    return largest

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    minLen = 0
    vars = csp.get_all_unasgn_vars()
    most = None
    # get list of all unassigned variables loop through
    for var in vars:
        # get number of legal values remaining
        legal = var.cur_domain_size()
        if minLen == 0 or legal < minLen:
            minLen = legal
            most = var
    return most
