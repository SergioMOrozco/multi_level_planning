from main import a_subset_b
import queue
import numpy as np
from main import mdp_2, mdp_1, mdp_0
from neighbourhood import Neighbourhood


class Planner():
    def __init__(self, options, N):
        self.options = options
        self.N = N
        # arr1 = np.zeros((8, 8))
        # arr1[1, 0] = 1
        # print(N(arr1))


    def extract_plan(self, state, parents):
        route = []
        state = self.to_tuple(state)
        while parents[state] != None:
            prev_option_term_state, option, option_start_state = parents[state]
            route = [(option_start_state, option)] + route
            state = self.to_tuple(prev_option_term_state)
        return route

    # termination conditions are an OR, which makes neighbourhoods an intersection rather than subset
    def get_sucessors(self, S): #format: [sucessor, option]
        sucessors = []
        reached = []
        for option in self.options:
            for state in option.list_initiation_states():
                
                if a_subset_b(S, self.N(state)):
                    
                    term_state = option.execute_policy(state)
                    if self.to_tuple(term_state) not in reached:
                        sucessors.append([term_state, option, state])
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
        frontier = queue.Queue() 
        
        parents = {self.to_tuple(S):None} #parents format -> state:[previous_state, option used]
        frontier.put(S)
        while (not frontier.empty()):
            state = frontier.get()
            for i in self.get_sucessors(state):
                state_to_tup = self.to_tuple(i[0])
                if a_subset_b(i[0], self.N(G)):
                    parents[self.to_tuple(i[0])] = [state, i[1], i[2]]
                    return True, self.extract_plan(i[0], parents)
                    
                elif state_to_tup not in reached:
                    reached.append(state_to_tup)
                    parents[self.to_tuple(i[0])] = [state, i[1], i[2]]
                    frontier.put(i[0])
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
