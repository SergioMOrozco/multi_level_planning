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
        self.stitches_store = {}
        # arr1 = np.zeros((8, 8))
        # arr1[1, 0] = 1
        # print(N(arr1))

    def count_stitches(self, state, parents): #count the number of gaps needing to be stiched on the path to state
        state = self.to_tuple(state)
        if state not in parents:
            print("PANIC, state should have been in parents")
            return
        if parents[state] == None: #we are at the root
            return 0
        if state in self.stitches_store:
            return self.stitches_store[state]
        prev_option_term_state, option, option_start_state = parents[state]
        num_stitches_to_parent = self.count_stitches(prev_option_term_state, parents)
        if np.array_equal(prev_option_term_state, option_start_state):
            self.stitches_store[state] = num_stitches_to_parent
        else:
            self.stitches_store[state] = num_stitches_to_parent + 1
        return self.stitches_store[state]

        
        


    def extract_plan_efficiency(self, state, parents): # returns [plan length, number of gaps stitched]
        # state:[previous_state, option used, state from which option executed]
        state1 = state
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
        # print("term state \n", state)
        # if plan_len == 1:
        #     print("BLAH \n:",  pretty_print_plan(self.extract_plan(state1, parents)))
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
                    # if option.name == "room_2_quad_3->room_2_quad_4":
                    #     print("HERE:", S)
                    
                    term_state = option.execute_policy(state)
                    #REDUNDANCY HERE
                    #if self.to_tuple(term_state) not in reached:
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
        reached_in_epoch = []
        frontier1 = queue.Queue() 
        frontier2 = queue.Queue()
        goal_reached = False
        cur_efficiency = math.inf
        term_state = None
        parents = {self.to_tuple(S):None} #parents format -> state:[previous_state, option used, state from which option executed]
        frontier1.put(S)
        epoch = 0
        while (True):
            print("EPOCH:", epoch)
            epoch += 1
            if frontier1.empty():
                if goal_reached:
                    return True, self.extract_plan(term_state, parents)
                elif frontier2.empty():
                    break
                else:
                    frontier1 = frontier2
                    frontier2 = queue.Queue()
                    reached += reached_in_epoch
                    reached_in_epoch = []
            state = frontier1.get()
            stitches_to_state = self.count_stitches(state, parents)
            #print(self.get_sucessors(state))
            for i in self.get_sucessors(state):
                state_to_tup = self.to_tuple(i[2])
                stitches_to_i_new = stitches_to_state + (not np.array_equal(state, i[1]))
                # if state_to_tup[1][2] == 1:
                #     print("the i1: ", i[1], stitches_to_state, stitches_to_i_new)
                
                if a_subset_b(i[2], self.N(G)):
                    goal_reached = True
                    new_efficiency = stitches_to_i_new + (not a_subset_b(i[2], G))
                    if new_efficiency <= cur_efficiency:
                        term_state = i[2]
                        parents[state_to_tup] = [state, i[0], i[1]]
                        cur_efficiency = new_efficiency



                    # if self.to_tuple(i[2]) in parents:
                    #     old_parent  = parents[self.to_tuple(i[2])]
                    # else:
                    #     old_parent = None
                    # parents[self.to_tuple(i[2])] = [state, i[0], i[1]]
                    # new_efficiency = self.extract_plan_efficiency(i[2], parents)
                    # if new_efficiency <= cur_efficiency:
                    #     term_state = i[2]
                    #     print("eff:" , new_efficiency)
                    #     cur_efficiency = new_efficiency
                    # else:
                    #     parents[self.to_tuple(i[2])] = old_parent
                    
                #need to fix this              
                elif state_to_tup not in (reached + reached_in_epoch) or (state_to_tup in reached_in_epoch and self.count_stitches(state_to_tup, parents) > stitches_to_i_new):
                    reached_in_epoch.append(state_to_tup)
                    parents[state_to_tup] = [state, i[0], i[1]]
                    
                    frontier2.put(i[2]) #frontier may have duplicates
        return False, []

def pretty_print_plan(plan):
    for i in plan:
        print("state: \n", i[0])
        print("OPTION INFO")
        print(i[1].name)
        print("end state")
        print(i[1].execute_policy(i[0]))


if __name__ == "__main__":
    neigh = Neighbourhood()

    planner = Planner(mdp_1, neigh.N1)
    arr1 = np.zeros((8, 8))
    arr1[1, 1] = 1
    arr2 = np.zeros((8, 8))
    arr2[2, 4] = 1
    for i in planner.bfs_plan(arr1, arr2)[1]:
        print("state: \n", i[0])
        print("OPTION INFO")
        print(i[1].name)
        print("end state")
        print(i[1].execute_policy(i[0]))
        # print("start : \n", i[1].I)
        # print("to: \n", i[1].beta)
        # print("###############")
