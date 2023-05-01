import numpy as np
from copy import copy


#using inbuilt functions could speed this up. Also using some tuples instead of lists so that we can cache values

subset_cache = {}
def a_subset_b(a,b):
    # if (a, b) in subset_cache:
    #     return subset_cache[(a, b)]
    overlap = 0
    for i in a:
        if i in b:
            overlap += 1

    subset = overlap  == len(a)
    # subset_cache[(a, b)] = (subset, overlap)
    return subset,overlap

def a_intersects_b(a,b):
    overlap = 0
    for i in a:
        if i in b:
            overlap += 1

    intersects = overlap > 0

    return intersects, overlap


def matrix_to_list(matrix):

    states = np.argwhere(matrix == 1)

    return states.tolist()#tuple(map(tuple, states)) #states.totu()

def construct_graph(options_as_dict, modified_options,probabilistic):
    graph = {}
    for a in modified_options:
        for b in modified_options:
            if probabilistic:
                intersects, overlap = a_intersects_b(a.termination_as_list,b.initiation_as_list) 
                if intersects:
                    is_subset,_ = a_subset_b(options_as_dict[a.name].termination_as_list, options_as_dict[b.name].initiation_as_list)
                    is_gap = is_subset == False
                    if not a.name in graph.keys():
                        graph[a.name] = []
                    graph[a.name].append([b,overlap,is_gap])
            else:
                subset, overlap = a_subset_b(a.termination_as_list,b.initiation_as_list)
                if subset:
                    is_subset,_ = a_subset_b(options_as_dict[a.name].termination_as_list, options_as_dict[b.name].initiation_as_list)
                    is_gap = is_subset == False
                    if not a.name in graph.keys():
                        graph[a.name] = []
                    graph[a.name].append([b,overlap,is_gap])
    return graph

# successors of some set of states
def start_as_key_value(state_as_list,options_as_dict,modified_options,probabilistic):
    key = "start"
    value = []
    for a in modified_options:
        if probabilistic:
            intersects, overlap = a_intersects_b(state_as_list,a.initiation_as_list) 
            if intersects:
                is_subset,_ = a_subset_b(state_as_list, options_as_dict[a.name].initiation_as_list)
                is_gap = is_subset == False
                value.append([a,overlap,is_gap])
        else:
            subset, overlap = a_subset_b(state_as_list,a.initiation_as_list) 
            if subset:
                is_subset,_ = a_subset_b(state_as_list, options_as_dict[a.name].initiation_as_list)
                is_gap = is_subset == False
                value.append([a,overlap,is_gap])

    return key,value

def modify_options(options, neighborhood_function):
    modified_options = []

    for o in options:
        modified_o = copy(o)
        modified_o.I = neighborhood_function(o.I)
        modified_o.initiation_as_list = matrix_to_list(modified_o.I)
        modified_options.append(modified_o)

    return modified_options
