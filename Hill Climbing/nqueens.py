# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 14:50:00 2020
CS 540 hw3 nqueens.py
@author: Yucheng Lin; lin364
"""

import copy
import random
# =============================================================================
#     given a state of the board, return a list of all valid successor states
# =============================================================================
def succ(state, static_x, static_y):
    #ensure static point is a queen
    if state[static_x] != static_y:
        return []
    lists = []
    a = []
    b = []
    N = len(state)
    # x - index; y - value; interate through the state
    for x, y in enumerate (state):
        #if it is static point, don't move
        if x == static_x:
            pass
        else: # if not static point, move
            if y == 0:
                # if value 0, one successor, go up
                a = copy.copy(state)
                a[x] = 1
                lists.append(a)
                # if value N-1, one successor, go down
            elif y == N-1:
                a = copy.copy(state)
                a[x] = N-2
                lists.append(a)
            else: # other value, two successors, up or down
                a = copy.copy(state)
                a[x] += 1
                lists.append(a)
                b = copy.copy(state)
                b[x] -= 1
                lists.append(b)
    lists = sorted(lists)
    return lists
    
# =============================================================================
#     given a state of the board, 
#     return an integer score such that the goal state scores 0
# =============================================================================
def f(state):
    f = 0
    for x1, y1 in enumerate(state):
        for x2, y2 in enumerate(state):
            if x1 == x2: # same tile
                pass
            elif y1 == y2: # same row
                f += 1
                break
            elif abs(x1 - x2) == abs(y1 - y2): # same diagonal
                f +=1
                break
            else:
                pass
    return f

# =============================================================================
#     given the current state, use succ() to generate the successors 
#     and return the selected next state
# =============================================================================
def choose_next(curr, static_x, static_y):
    #ensure static point is a queen
    if curr[static_x] != static_y:
        return None
    lists = succ(curr, static_x, static_y)
    # add curr to the "lists" and form a new "lists" which include curr
    lists.append(curr)
    lists = sorted(lists)
    f_lowest = f(lists[0])
    f_lowest_idx = 0
    # iterate through the new list, find the first and lowest state
    for idx, state in enumerate (lists):
        if f(state) < f_lowest:
            f_lowest = f(state)
            f_lowest_idx = idx
    return lists[f_lowest_idx]

# =============================================================================
#     run the hill-climbing algorithm from a given initial state, 
#     return the convergence state
# =============================================================================
def n_queens(initial_state, static_x, static_y, print_path=True):
    state = initial_state
    x = static_x
    y = static_y
    fval = f(state)
    if print_path:
        print(f'{state} - f={fval}')
    # keep using choose_next, until it finds f=0 or a local optima
    while True:
        next_state = choose_next(state, x, y)
        next_fval = f(next_state)
        if print_path:
            print(f'{next_state} - f={next_fval}')
        # if f is 0
        if (next_fval == 0):
            return next_state
        # if f value is the same as the last one
        elif fval == next_fval:
            return next_state
        # keep moving, change state to next_state
        state = next_state
        fval = next_fval

# =============================================================================
#     run the hill-climbing algorithm on an n*n board with random restarts
# =============================================================================
def n_queens_restart(n, k, static_x, static_y):
    random.seed(1)
    
    best_states = []
    best_fval = n
    # loop until k times are used up or f reaches 0
    while k != 0:
        initial_state = []
        # create a random state, len=n
        for i in range(0, n):
            random_int = random.randint(0, n-1)
            initial_state.append(random_int)
        # set static point for the state
        initial_state[static_x] = static_y
        # get lowest state by n_queens
        state = n_queens(initial_state, static_x, static_y, False)
        fval = f(state)
        if fval == 0: # when f reaches 0, print and quit
            print(f'{state} - f={fval}')
            return
        elif fval < best_fval: 
            # update the solutions if fval should be renewed
            best_states.clear()
            best_states.append(state)
            best_fval = fval
        elif fval == best_fval: 
            # add the state to the solutions if the fval == best_fval
            best_states.append(state)
        k -= 1
    # after loop k times without reaching f=0, sort solutions
    best_states = sorted(best_states)
    # print solutions
    for s in best_states:
        print(f'{s} - f={best_fval}')
    
    
        
            
            
    
    
    
    
    
    