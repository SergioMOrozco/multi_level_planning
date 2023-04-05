import numpy as np
from neighbourhood import Neighbourhood
from main import a_subset_b


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

    def hierarchical_plan(self, S, G, i):
        if i < 0:
            return False, []
        # no plan_match needed atm as there are no state abstractions currently
        N = self.neighbourhood_function(i)
        result, plan = planner(S, N(G)) #PLAN WITH NEIGHBOURHOODS HERE
        plan_len = len(plan)
        # the plan should be a sequence of options
        if not result:
            return self.hierarchical_plan(S, G, i-1)
        # TO-DO: ADD IS PLAN EFFECTIVE

        #stitching the gaps
        index = 0
        if not a_subset_b(S, plan[0].I): #stitching gap at start
            result, sub_plan = self.hierarchical_plan(S, plan[0].I, i - 1)
            if result == False:
                return False, []
            else:
                plan = sub_plan + plan
                index += len(sub_plan) + 1
        for i in range(plan_len - 1): #stitching intermediate gaps
            if not a_subset_b(plan[index].beta, plan(index + 1).I):
                result, sub_plan = self.hierarchical_plan(plan[index].beta, plan(index + 1).I, i - 1)
                if result == False:
                    return False, []
                else:
                    plan = plan[:i+1] + sub_plan + plan[i+1:]
                    index += len(sub_plan) + 1
        if not a_subset_b(plan[-1].beta, G): #stitching gap at end
            result, sub_plan = self.hierarchical_plan(plan[-1].beta, G, i - 1)
            if result == False:
                return False, []
            else:
                plan =  plan + sub_plan
        return True, plan
    

            



        