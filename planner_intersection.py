import queue
import numpy as np
import math
from main import mdp_2, mdp_1, mdp_0
from neighbourhood import Neighbourhood
from utils import construct_graph, modify_options, a_subset_b, matrix_to_list, start_as_key_value, a_intersects_b

class PlannerIntersection():
    def __init__(self, options_as_dict, N, probabilistic, modified_options, modified_graph):
        self.options_dict = options_as_dict
        self.probabilistic = probabilistic

        #self.modified_options = modify_options(options, N)
        self.modified_options = modified_options 

        self.neighbourhood_function = N

        #self.modified_graph = construct_graph(self.modified_options)
        self.modified_graph = modified_graph 

    def check(self, a_as_list, b_as_list):
        if self.probabilistic:

            return a_intersects_b(a_as_list,b_as_list)

        return a_subset_b(a_as_list,b_as_list)

    def extract_plan(self, name, parents): #backtrack using parents and return the plan
        route = []

        parent_name = name

        total_overlap = 0
        total_gaps = 0

        while parents[parent_name] != None:
            parent_name, option,overlap, is_gap = parents[parent_name]

            total_overlap += overlap

            if is_gap:
                total_gaps += 1

            # TODO: option needs to be regular option
            route.insert(0,self.options_dict[option.name])

        return route, total_overlap,total_gaps #format: [state from which option executed, option]

    def bfs_plan(self, S, G):
        """
        Implement breadth-first search.
        Input:
            problem - the problem on which the search is conducted, a SearchProblem
        Output: a list of states representing the path of the solution
        """
        s_as_list = matrix_to_list(S)
        g_as_list = matrix_to_list(G)
        modified_g_as_list = matrix_to_list(self.neighbourhood_function(G))
        max_depth = math.inf
        plans = []

        # we are already at goal state
        check , _= self.check(s_as_list,g_as_list)
        if check:
            print("start is alread at goal")
            return True, []

        frontier = queue.Queue() 

        s_key, s_value = start_as_key_value(s_as_list,self.options_dict,self.modified_options,self.probabilistic)

        #print(s_key,s_value)

        reached = [s_key]
        self.modified_graph[s_key] = s_value
        parents = {s_key:None} 


        frontier.put([s_key,1])
        while (not frontier.empty()):

            key, depth = frontier.get()

            for value_option,overlap,is_gap in self.modified_graph[key]:

                if self.check(value_option.termination_as_list,modified_g_as_list)[0] and depth <= max_depth:
                    parents[value_option.name] = [key,value_option,overlap,is_gap]

                    if max_depth == math.inf:
                        max_depth = depth

                    plan, total_overlap, total_gaps = self.extract_plan(value_option.name, parents)
                    plans.append([plan,total_overlap,total_gaps, depth])

                    reached.append(value_option.name)

                    #return True, plan
                    
                elif not value_option.name in reached:

                    reached.append(value_option.name)
                    parents[value_option.name] = [key,value_option, overlap, is_gap]
                    frontier.put([value_option.name,depth +1])

        best_plan = []
        max_overlap = 0
        min_gaps = math.inf

        for plan,overlap,gaps,depth in plans:
            if overlap >= max_overlap and gaps <= min_gaps:
                best_plan = plan
                max_overlap = overlap
                min_gaps = gaps

        # for o in best_plan:
        #     print(o.name)
        #     print(o.I)
        #     print(o.beta)
        #
        # print("OVERLAP:" + str(overlap))
        # print("GAPS:" + str(gaps))

        if best_plan == []:
            print("fail")

        return not best_plan == None, best_plan

if __name__ == "__main__":
    neigh = Neighbourhood()

    planner = PlannerIntersection(mdp_1, neigh.N1)
    #planner = PlannerIntersection(mdp_0, neigh.N0)
    # arr1 = np.zeros((8, 8))
    # arr1[4, 3] = 1
    # arr2 = np.zeros((8, 8))
    # arr2[6, 3] = 1
    arr1 = np.zeros((8, 8))
    arr1[1, 1] = 1
    arr2 = np.zeros((8, 8))
    arr2[7, 7] = 1

    current = arr1
    for option in planner.bfs_plan(arr1, arr2)[1]:
        print("state: \n", current)
        print("OPTION INFO")
        print(option.name)
        print("end state")
        current = option.execute_policy(current)
        print(current)
        print("start : \n", option.I)
        print("to: \n", option.beta)
        print("###############")
