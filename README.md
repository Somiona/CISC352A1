# Assignment 1: CSPs


Welcome to the first assignment! You can find the description PDF attached, as well as the starter code ZIP file and some documentation for the main chunk of code you'll interface with. Any questions should be directed first and foremost to the forum, and if it's too personal in nature (i.e., would reveal your code), you can email the assignment TA listed on the onQ landing page.

## Acceptable Imports
Python can pretty much do anything with the right import. This is why you aren't allowed to import random things for your assignment, since the problem may be trivially solvable. However, some functions are useful and kind of a pain to re-implement (and it also covers things we don't really care to teach/assess here). These are the only allowable imports (if you want something added to the list, you must reach out to the TA/prof to check):

- itertools.permutations
- itertools.product
- itertools.combination
- math.prod
- collections.defaultdict
- operator.itemgetter

## Question 1: Propagators and Heuristics

- [ ] prop FC (worth 1/6 marks)
A propagator function that propagates according to the FC algorithm that check constraints that have exactly one variable in their scope that has not assigned with a value, and prune appropriately. If `newVar` is None, forward check all constraints. Otherwise only check constraints containing `newVar`.

- [ ] prop GAC (worth 1.5/6 marks)
A propagator function that propagates according to the GAC algorithm, as covered in lecture. If `newVar` is None, run GAC on all constraints. Otherwise, only check constraints containing `newVar`.

- [ ] ord mrv (worth 0.5/6 marks)
A variable ordering heuristic that chooses the next variable to be assigned according to the Minimum Remaining-Value (MRV) heuristic. ord mrv returns the variable with the most constrained current domain (i.e., the variable with the fewest legal values remaining).

- [ ] ord dh (worth 0.5/6 marks)
A variable ordering heuristic that chooses the next variable to be assigned according to the Degree heuristic (DH). ord dh returns the variable that is involved in the largest number of constraints, which have other unassigned variables

## Question 2: Models
- [x] binary ne grid (worth 0.5/6 marks)
A model of a Cagey grid (without cage constraints) built using only binary not-equal constraints for both the row and column constraints.

- [x] nary ad grid (worth 0.5/6 marks)
A model of a Cagey grid (without cage constraints) built using only n-ary all-different constraints for both the row and column constraints.

- [x] cagey csp model (worth 1/6 marks)
A model built using your choice of (1) binary binary not-equal, or (2) n-ary all-different constraints for the grid, together with (3) cage constraints. That is, you will choose one of the previous two grid models and expand it to include cage constraints.
