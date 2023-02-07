# =============================
# Student Names: Jihyeon Park
# Group ID: 23
# Date:
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''

    #this is for retrieving all the constraints
    if newVar:
        cons = csp.get_cons_with_var(newVar)
    else:
        cons = csp.get_all_cons()

    #all the pruned values will be stored in this list
    pruned = []

    '''
    this block will detect an unassigned value 
    in each constraint and determine the pruned values and the validity of csp
    '''
    for con in cons:
        #looking for a constraint that has only one unassigned variable
        if con.get_n_unasgn() == 1:
            vars = con.get_unasgn_vars()
            #this is the unassigned variable
            var = vars[0]
            '''
            this for loop is for pruning the invalid values in the domain
            if the current domain size is zero, the function will return False and all the pruned values
            '''
            for val in var.cur_domain():
                #if the value does not satisfy, it will be pruned
                if not con.check_var_val(var, val):
                    var.prune_value(val)
                    prune = (var, val)
                    if prune not in pruned:
                        pruned.append(prune)
                #this is the case where the current domain size is zero
                if var.cur_domain_size() == 0:
                    return False, pruned

    #this function returns True if there is no problem.
    return True, pruned

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    # this is for retrieving all the constraints
    if newVar:
        cons = csp.get_cons_with_var(newVar)
    else:
        cons = csp.get_all_cons()

    # all the pruned values will be stored in this list
    pruned = []

    #this queue is for storing all the constraints
    gac_queue = []
    for con in cons:
        gac_queue.append(con)

    #This block is for detecting the problems in the csp and prune all the values
    while gac_queue:
        #remove the first constraint from the queue
        curr_con = gac_queue[0]
        gac_queue = gac_queue[1:]
        #this is for getting all the unassigned variables
        vars = curr_con.get_unasgn_vars()

        '''
        this for loop is for trying a value for an assigned variable.
        then, this for loop will the other neighboring unassigned variables
        '''
        for var in vars:
            #try one value for an assigned variable
            for val in var.cur_domain():
                #check the other unassigned variable in the constraint
                for other_var in vars:
                    for other_val in other_var.cur_domain():
                        #this is for pruning values in some values in other variable that do not satisfy the constraint
                        if not curr_con.check_var_val(other_var, other_val):
                            other_var.prune_value(other_val)
                            prune = (other_var, other_val)
                            if prune not in pruned:
                                pruned.append(prune)
                        #this is the case where the current domain size is zero.
                        if other_var.cur_domain_size() == 0:
                            return False, pruned

    return True, pruned
