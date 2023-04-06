import numpy as np
from neighbourhood import Neighbourhood
from main import a_subset_b, mdp_2, mdp_1, mdp_0
from planner import Planner


class Hierarchical_plan():
    def __init__(self):
        self.neighbourhood = Neighbourhood()

    def neighbourhood_function(self, i): #r eturns the neighbourhood_function for the ith level of abstraction
        if i == 0:
            return self.neighbourhood.N0
        elif i == 1:
            return self.neighbourhood.N1
        elif i == 2:
            return self.neighbourhood.N2
        else:
            print("ERROR")
    
    def options(self, i): #r eturns the neighbourhood_function for the ith level of abstraction
        if i == 0:
            return mdp_0
        elif i == 1:
            return mdp_1
        elif i == 2:
            return mdp_2
        else:
            print("ERROR")

    def hierarchical_plan(self, S, G, i):
        if i < 0:
            print("THIS SHOULD NOT HAPPEN")
            return False, []

        # no plan_match needed atm as there are no state abstractions currently
        N = self.neighbourhood_function(i)
        options = self.options(i)
        planner = Planner(options, N)
        if a_subset_b(S, N(G)):
            return self.hierarchical_plan(S, G, i-1)
        result, plan = planner.bfs_plan(S, G) #PLAN WITH NEIGHBOURHOODS HERE
        # format of plan is [start_state, option]
        plan_len = len(plan)
        # the plan should be a sequence of options
        if not result:
            return self.hierarchical_plan(S, G, i-1)
        # TO-DO: ADD IS PLAN EFFECTIVE
        #stitching the gaps
        index = 0
        if not a_subset_b(S, plan[0][0]): #stitching gap at start
            result, sub_plan = self.hierarchical_plan(S, plan[0][0], i - 1)
            if result == False:
                return False, []
            else:
                plan = sub_plan + plan
                index += len(sub_plan)
        for x in range(plan_len - 1): #stitching intermediate gaps
            beta = plan[index][1].execute_policy(plan[index][0])
            I = plan[index + 1][0]
            if not a_subset_b(beta, I):
                result, sub_plan = self.hierarchical_plan(beta, I, i - 1)
                if result == False:
                    # print(beta, I)
                    return False, []
                else:
                    plan = plan[:index+1] + sub_plan + plan[index+1:]
                    index +=  1 + len(sub_plan)
            else:
                index += 1
        #stitching gap at end
        beta = plan[-1][1].execute_policy(plan[-1][0])
        if not a_subset_b(beta, G): 
            result, sub_plan = self.hierarchical_plan(beta, G, i - 1)
            # if i == 2:
            #     print(sub_plan)
            if result == False:
                return False, []
            else:
                plan =  plan + sub_plan
        return True, plan

if __name__ == "__main__":
    hp_planner = Hierarchical_plan()
    arr1 = np.zeros((8, 8))
    arr1[0, 0] = 1 #set start state
    arr2 = np.zeros((8, 8))
    arr2[6, 7] = 1 #set goal state
    plan = hp_planner.hierarchical_plan(arr1, arr2, 2)
    for i in plan[1]:
        print(i[0])
        print(i[1].name)
    print(arr2)