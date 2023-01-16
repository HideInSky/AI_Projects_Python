# -*- coding: utf-8 -*-
"""
CS 540 2020 Fall HW1 - statespace
@author: Yucheng Lin
"""

def fill(state, max, which):
    #copy the state
    return_state = [0,0]
    return_state[0] = state[0]
    return_state[1] = state[1]    
    return_state[which] = max[which]
    return return_state

def empty(state, max, which):
    #copy the state
    return_state = [0,0]
    return_state[0] = state[0]
    return_state[1] = state[1]
    return_state[which] = 0
    return return_state

def xfer(state, max, source, dest):
    #copy the state
    return_state = [0,0]
    return_state[0] = state[0]
    return_state[1] = state[1]
    #if the source+dest <= capacity of dest
    if return_state[source] + return_state[dest] <= max[dest]:
        #source = 0, add dest
        return_state[dest] += return_state[source]
        return_state[source] = 0
    else:
        #dest full, source decrease
        return_state[source] += return_state[dest]
        return_state[source] -= max[dest]
        return_state[dest] = max[dest]
    return return_state

def succ(state, max):
    #show result of fill, empty and xfer
    result = [fill(state, max, 0), fill(state, max, 1),\
    empty(state, max, 0), empty(state, max, 1),\
    xfer(state, max, 1, 0), xfer(state, max, 0, 1)]
    result2 = []
    for i in result:
        if not i in result2:
            result2.append(i)
    print(result2)
