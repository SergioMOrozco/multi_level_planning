import queue
import numpy as np
import math
from main import mdp_2, mdp_1, mdp_0
from neighbourhood import Neighbourhood
from planner import Planner
from utils import construct_graph, modify_options, a_subset_b, matrix_to_list, start_as_key_value, a_intersects_b

class PlannerNaive():
    def __init__(self, options_as_dict, options, graph):
        self.options_dict = options_as_dict
        self.options = options
        self.graph = graph
       

    def check(self, a_as_list, b_as_list):
        return a_subset_b(a_as_list,b_as_list)

    def extract_plan(self, name, parents): #backtrack using parents and return the plan
        route = []

        parent_name = name

        while parents[parent_name][0] != None:
            parent_name, option = parents[parent_name]
            # TODO: option needs to be regular option
            route.insert(0,self.options_dict[option.name])

        return route


    def bfs_plan(self, S, G):
        """
        Implement breadth-first search.
        Input:
            problem - the problem on which the search is conducted, a SearchProblem
        Output: a list of states representing the path of the solution
        """
        s_as_list = matrix_to_list(S)
        g_as_list = matrix_to_list(G)

        # we are already at goal state
        check , _= self.check(s_as_list,g_as_list)
        if check:
            print("start is alread at goal")
            return []

        frontier = queue.Queue() 

        s_key, s_value = start_as_key_value(s_as_list,self.options_dict,self.options, False)

        #print(s_key,s_value)
        reached = set()
        reached.add(s_key)
        self.graph[s_key] = s_value
        parents = {s_key: [None, None]}

        frontier.put(s_key)
        while (not frontier.empty()):

            key = frontier.get()
    

            for value_option, _, _ in self.graph[key]:
        

                if self.check(value_option.termination_as_list,g_as_list)[0]:
                    parents[value_option.name] = [key,value_option]
                    best_plan = self.extract_plan(value_option.name, parents)
                    return best_plan
                    
                elif not value_option.name in reached:
                    reached.add(value_option.name)
                    parents[value_option.name] = [key,value_option]
                    frontier.put(value_option.name)

        

        

        return []
    

if __name__ == "__main__":
    options_dict = {}
    for o in mdp_0:
        options_dict[o.name] = o
    planner = PlannerNaive(options_dict, mdp_0, construct_graph(options_dict, mdp_0, False))
    arr1 = np.zeros((8, 8))
    arr1[1, 1] = 1
    arr2 = np.zeros((8, 8))
    arr2[7, 7] = 1
    plan = planner.bfs_plan(arr1, arr2)
    for o in plan:
        print(o.name)

    
