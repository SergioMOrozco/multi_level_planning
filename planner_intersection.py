import queue
import numpy as np
import math
from main import mdp_2, mdp_1, mdp_0
from neighbourhood import Neighbourhood
from utils import construct_graph, modify_options, a_subset_b, matrix_to_list, start_as_key_value, a_intersects_b

class PlannerIntersection():
    def __init__(self, options_as_dict, N, probabilistic, modified_options, modified_graph, planner_alpha = 0):
        self.options_dict = options_as_dict
        self.probabilistic = probabilistic

        #self.modified_options = modify_options(options, N)
        self.modified_options = modified_options 

        self.neighbourhood_function = N
        self.alpha = planner_alpha #ideally planner_apha = alpha[from is plan effective]/plan_time_per_neighbourhood
        #self.modified_graph = construct_graph(self.modified_options)
        self.modified_graph = modified_graph 

    def check(self, a_as_list, b_as_list):
        if self.probabilistic:

            return a_intersects_b(a_as_list,b_as_list)

        return a_subset_b(a_as_list,b_as_list)

    def extract_plan(self, name, parents): #backtrack using parents and return the plan
        route = []

        parent_name = name

        total_overlap = 1
        total_gaps = 0

        while parents[parent_name][0] != None:
            parent_name, option,overlap, is_gap = parents[parent_name]
            # if parent_name == "start": #bad code, fix this
            #     beta_len = 1
            # else:
            #     beta_len = len(self.options_dict[parent_name].termination_as_list)

            # total_overlap *= overlap/ beta_len

            # if is_gap:
            #     total_gaps += 1

            # TODO: option needs to be regular option
            route.insert(0,self.options_dict[option.name])

        return route

    def plan_score(self, key, parents):
        _, _, overlap, num_gaps = parents[key]
        return num_gaps - self.alpha * overlap

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
            return True, [], 0, 1

        frontier = queue.Queue() 

        s_key, s_value = start_as_key_value(s_as_list,self.options_dict,self.modified_options,self.probabilistic)

        #print(s_key,s_value)

        reached = [s_key]
        reached_in_epoch = [s_key]
        self.modified_graph[s_key] = s_value
        parents = {s_key: [None, None, 1, 0]}
        term_state = None
        best_efficiency = math.inf
        best_overlap = None
        best_num_gaps = None

        frontier.put([s_key,1])
        cur_depth = 0

        while (not frontier.empty()):

            key, depth = frontier.get()
            _, option, p_overlap, p_num_gaps = parents[key]
            if option is None:
                option_beta = 1
            else:
                option_beta = len(option.termination_as_list)
            # parent_beta = self.options_dict[parent_name].beta

            if depth > max_depth:
                break
            if depth > cur_depth:
                cur_depth = depth
                reached_in_epoch = []

            for value_option,overlap,is_gap in self.modified_graph[key]:
                overlap *= p_overlap/option_beta
                num_gaps = p_num_gaps + is_gap

                if self.check(value_option.termination_as_list,modified_g_as_list)[0] and depth <= max_depth:
                    if max_depth == math.inf:
                        max_depth = depth
                    if term_state is None:
   
                        num_gaps +=  not a_subset_b(value_option.termination_as_list,g_as_list)[0]
                     
                        overlap *= a_intersects_b(value_option.termination_as_list, modified_g_as_list)[1] / len(value_option.termination_as_list)
                        parents[value_option.name] = [key,value_option,overlap,num_gaps]
                        term_state = value_option.name
                        best_overlap = overlap
                        best_num_gaps = num_gaps
                        best_efficiency = num_gaps - self.alpha * overlap
                    
                    else: 

                        num_gaps +=  not a_subset_b(value_option.termination_as_list,g_as_list)[0]
                        overlap *= a_intersects_b(value_option.termination_as_list, modified_g_as_list)[1] / len(value_option.termination_as_list)
                        if num_gaps - self.alpha * overlap <= best_efficiency:
                            parents[value_option.name] = [key,value_option,overlap,num_gaps]
                            term_state = value_option.name
                            best_overlap = overlap
                            best_num_gaps = num_gaps
                            best_efficiency = num_gaps - self.alpha * overlap
                    # plan, total_overlap, total_gaps = self.extract_plan(value_option.name, parents)
                    # plans.append([plan,total_overlap,total_gaps, depth])

                    reached.append(value_option.name)

                    #return True, plan
                    
                elif not value_option.name in reached or \
                    value_option.name in reached_in_epoch and self.plan_score(value_option.name, parents) > num_gaps - self.alpha * overlap:
                    reached.append(value_option.name)
                    reached_in_epoch.append(value_option.name)
                    parents[value_option.name] = [key,value_option, overlap, num_gaps]
                    frontier.put([value_option.name,depth +1])

        # best_plan = []
        # max_overlap = 0
        # min_gaps = math.inf

        # for plan,overlap,gaps,depth in plans:
        #     if gaps - self.alpha * overlap < min_gaps - self.alpha * max_overlap:
        #         best_plan = plan
        #         max_overlap = overlap
        #         min_gaps = gaps

        # for o in best_plan:
        #     print(o.name)
        #     print(o.I)
        #     print(o.beta)
        #
        # print("OVERLAP:" + str(overlap))
        # print("GAPS:" + str(gaps))

        

        if term_state == None:
            return False, [], 0, 1
        best_plan = self.extract_plan(term_state, parents)
        return not best_plan == None, best_plan, best_num_gaps, best_overlap

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
