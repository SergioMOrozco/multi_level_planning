from main import a_subset_b
import queue
import numpy as np
from main import mdp_2, mdp_1, mdp_0
from neighbourhood import Neighbourhood
import math


class Planner():
    def __init__(self, options, N):
        self.options = options
        self.N = N
        # arr1 = np.zeros((8, 8))
        # arr1[1, 0] = 1
        # print(N(arr1))

    def extract_plan_efficiency(self, state, parents): # returns [plan length, number of gaps stitched]
        # state:[previous_state, option used, state from which option executed]
        plan_len = 0
        num_gaps = 0
        state = self.to_tuple(state)
        if state not in parents:
            return [math.inf, math.inf]
        while parents[state] != None:
            prev_option_term_state, option, option_start_state = parents[state]
            plan_len += 1
            if not np.array_equal(prev_option_term_state, option_start_state):
                num_gaps += 1
            state = self.to_tuple(prev_option_term_state)
        return [plan_len, num_gaps]


    def extract_plan(self, state, parents): #backtrack using parents and return the plan
        # 
        route = []
        state = self.to_tuple(state)
        while parents[state] != None:
            prev_option_term_state, option, option_start_state = parents[state]
            route = [(option_start_state, option)] + route
            state = self.to_tuple(prev_option_term_state)
        return route #format: [state from which option executed, option]

    # termination conditions are an OR, which makes neighbourhoods an intersection rather than subset
    def get_sucessors(self, S): #format: [option, option_start_state, option_termination_state]
        sucessors = []
        reached = []
        for option in self.options:
            for state in option.list_initiation_states():
                
                if a_subset_b(S, self.N(state)):
                    
                    term_state = option.execute_policy(state)
                    if self.to_tuple(term_state) not in reached:
                        #state is in the neighbourhood of S, option is executed from state to term_state. The gap between S and state will be stitched on lower levels
                        #sucessors.append([term_state, option, state])
                        sucessors.append([option, state, term_state])
                        reached.append(self.to_tuple(term_state))
        return sucessors

    def to_tuple(self, S):
        return tuple(map(tuple, S))

    def bfs_plan(self, S, G):
        """
        Implement breadth-first search.
        Input:
            problem - the problem on which the search is conducted, a SearchProblem
        Output: a list of states representing the path of the solution
        """

        if a_subset_b(S, self.N(G)):
            return True, []
        reached = [self.to_tuple(S)]
        frontier1 = queue.Queue() 
        frontier2 = queue.Queue()
        goal_reached = False
        cur_efficiency = [math.inf, math.inf]
        term_state = None
        parents = {self.to_tuple(S):None} #parents format -> state:[previous_state, option used, state from which option executed]
        frontier1.put(S)
        while (True):
            if frontier1.empty():
                if goal_reached:
                    return True, self.extract_plan(term_state, parents)
                elif frontier2.empty():
                    break
                else:
                    frontier1 = frontier2
                    frontier2 = queue.Queue()
            state = frontier1.get()
            for i in self.get_sucessors(state):
                state_to_tup = self.to_tuple(i[2])
                if a_subset_b(i[2], self.N(G)):
                    goal_reached = True
                    if self.to_tuple(i[2]) in parents:
                        old_parent  = parents[self.to_tuple(i[2])]
                    else:
                        old_parent = None
                    parents[self.to_tuple(i[2])] = [state, i[0], i[1]]
                    new_efficiency = self.extract_plan_efficiency(i[2], parents)
                    if new_efficiency < cur_efficiency:
                        term_state = i[2]
                        cur_efficiency = new_efficiency
                    else:
                        parents[self.to_tuple(i[2])] = old_parent
                    
                    
                elif state_to_tup not in reached:
                    reached.append(state_to_tup)
                    parents[self.to_tuple(i[2])] = [state, i[0], i[1]]
                    frontier2.put(i[2])
        return False, []

if __name__ == "__main__":
    neigh = Neighbourhood()

    planner = Planner(mdp_1, neigh.N1)
    arr1 = np.zeros((8, 8))
    arr1[4, 3] = 1
    arr2 = np.zeros((8, 8))
    arr2[6, 3] = 1
    for i in planner.bfs_plan(arr1, arr2)[1]:
        print("state: \n", i[0])
        print("OPTION INFO")
        print(i[1].name)
        print("end state")
        print(i[1].execute_policy(i[0]))
        # print("start : \n", i[1].I)
        # print("to: \n", i[1].beta)
        # print("###############")