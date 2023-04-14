import numpy as np
from copy import copy

def a_subset_b(a,b):
    for i in a:
        if not i in b:
            return False
    return True
def a_intersects_b(a,b):
    for i in a:
        # need to know how much of an intersection
        if i in b:
            return True
    return False

def matrix_to_list(matrix):
    states = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1:
                states.append([i,j])
    return states

def construct_graph(options):
    graph = {}
    for a in options:
        for b in options:
            if a_intersects_b(a.termination_as_list,b.initiation_as_list):
                if not a.name in graph.keys():
                    graph[a.name] = []
                graph[a.name].append(b)
    return graph

# successors of some set of states
def start_as_key_value(state_as_list,options):
    key = "start"
    value = []
    for a in options:
        if a_subset_b(state_as_list,a.initiation_as_list):
            value.append(a)

    return key,value

def modify_options(options, neighborhood_function):
    modified_options = []

    for o in options:
        modified_o = copy(o)
        modified_o.I = neighborhood_function(o.I)
        modified_o.initiation_as_list = matrix_to_list(modified_o.I)
        modified_options.append(modified_o)

    return modified_options
