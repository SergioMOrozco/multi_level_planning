import numpy as np
import utils
import random
import time
from option import Option
from action import Action 
from neighbourhood import Neighbourhood
from utils import matrix_to_list, modify_options, construct_graph
from main import a_subset_b, mdp_2, mdp_1, mdp_0, mdp_2_p, mdp_1_p, mdp_0_sz, mdp_1_sz, mdp_2_sz, mdp_1_p_sz, mdp_2_p_sz
from planner import Planner
from planner_intersection import PlannerIntersection
from is_plan_effective import IsPlanEffective


class Hierarchical_plan():
    def __init__(self, probabilistic = False):
        self.neighbourhood = Neighbourhood("advanced", 4, 2, 1)
        self.probabilistic = probabilistic
        self.options_dicts = []
        options_dict_0 = {}
        options_dict_1 = {}
        options_dict_2 = {}

        for o in self.options(0):
            options_dict_0[o.name] = o
        for o in self.options(1):
            options_dict_1[o.name] = o
        for o in self.options(2):
            options_dict_2[o.name] = o

        self.options_dicts = [options_dict_0,options_dict_1,options_dict_2]

        self.modified_options = [modify_options(self.options(0),self.neighbourhood_function(0)),modify_options(self.options(1),self.neighbourhood_function(1)),modify_options(self.options(2),self.neighbourhood_function(2))]
        self.modified_graph = [construct_graph(options_dict_0,self.modified_options[0],probabilistic),construct_graph(options_dict_1,self.modified_options[1],probabilistic),construct_graph(options_dict_2,self.modified_options[2],probabilistic)]


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
            if self.probabilistic:
                return mdp_1_p
            return mdp_1
        elif i == 2:
            if self.probabilistic:
                return mdp_2_p
            return mdp_2
        else:
            print("ERROR")
    
    def num_options(self, i): #r eturns the neighbourhood_function for the ith level of abstraction
        if self.probabilistic:
            if i == 0:
                return mdp_0_sz
            elif i == 1:
                return mdp_1_p_sz
            elif i == 2:
                return mdp_2_p_sz
            else:
                print("ERROR")
        if i == 0:
            return mdp_0_sz
        elif i == 1:
            return mdp_1_sz
        elif i == 2:
            return mdp_2_sz
        else:
            print("ERROR")
        
    def option_sz(self, i):
        if i == 0:
            return self.neighbourhood.l0
        if i == 1:
            return self.neighbourhood.l1
        if i == 2:
            return self.neighbourhood.l2
        print("ERROR")

    def neighbourhood_sz(self, i):
        if i == 0:
            return self.neighbourhood.N0_sz
        if i == 1:
            return self.neighbourhood.N1_sz
        if i == 2:
            return self.neighbourhood.N2_sz
        print("ERROR")



    def hierarchical_plan_v1(self, S, G, i):

        if i < 0:
            print("THIS SHOULD NOT HAPPEN")
            return False, []

        # no plan_match needed atm as there are no state abstractions currently
        N = self.neighbourhood_function(i)
        options = self.options(i)
        planner = Planner(options, N)
        if a_subset_b(S, N(G)):
            return self.hierarchical_plan_v1(S, G, i-1)
        result, plan, num_gaps = planner.bfs_plan(S, G) #PLAN WITH NEIGHBOURHOODS HERE
        # format of plan is [start_state, option]
        plan_len = len(plan)
        # the plan should be a sequence of options
        if not result: # drop to a lower level
            print("PLAN FAILED, DROPPING TO LOWER LEVEL")
            return self.hierarchical_plan_v1(S, G, i-1)
        # TO-DO: ADD IS PLAN EFFECTIVE

        if i is not 0:
            num_options = self.num_options(i - 1)
            neighbourhood_sz = self.neighbourhood_sz(i)
            option_sz = self.option_sz(i - 1)
            IPE = IsPlanEffective(option_sz, num_options, neighbourhood_sz)
            if not IPE.is_plan_effective(num_gaps, S, G):
                print("PLAN IS NOT EFFECTIVE, DROPPING TO LOWER LEVEL")
                return self.hierarchical_plan_v1(S, G, i-1)
        #stitching the gaps
        index = 0
        if not a_subset_b(S, plan[0][0]): #stitching gap at start
            result, sub_plan = self.hierarchical_plan_v1(S, plan[0][0], i - 1)
            if result == False:
                print("FAILURE")
                return False, []
            else:
                plan = sub_plan + plan
                index += len(sub_plan)
        for x in range(plan_len - 1): #stitching intermediate gaps
            beta = plan[index][1].beta
            I = plan[index + 1][0]
            if not a_subset_b(beta, I):
                result, sub_plan = self.hierarchical_plan_v1(beta, I, i - 1)
                if result == False:
                    print("FAILURE")
                    # print(beta, I)
                    return False, []
                else:
                    plan = plan[:index+1] + sub_plan + plan[index+1:]
                    index +=  1 + len(sub_plan)
            else:
                index += 1
        #stitching gap at end
        beta = plan[-1][1].beta
        if not a_subset_b(beta, G): 
            result, sub_plan = self.hierarchical_plan_v1(beta, G, i - 1)
            # if i == 2:
            #     print(sub_plan)
            if result == False:
                print("FAILURE")
                return False, []
            else:
                plan =  plan + sub_plan
        return True, plan

    def __stitch_gaps(self,start_as_matrix, goal_as_matrix,i):
        # print(S)
        # print(plan[0].I)
        # print("start is not subset of " + plan[0].name)

        start_as_list = matrix_to_list(start_as_matrix)

        possible_plans = []

        # This print statement is an easy check for probabilistic planning
        #print(len(start_as_list))
        for j in range(len(start_as_list)):
            state = start_as_list[j]

            possible = np.zeros((8, 8))
            possible[state[0],state[1]] = 1
            result, sub_plan = self.hierarchical_plan_v2(possible, goal_as_matrix, i - 1)
            if result == False:
                print("FAILURE1")
                return False, []

            possible_plans.append(sub_plan)

        return possible_plans

    def hierarchical_plan_v2(self, S, G, i):
        #To-DO: Tune hyperparameter values

        if i < 0:
            print("THIS SHOULD NOT HAPPEN")
            return False, []

        N = self.neighbourhood_function(i)

        start_as_list = matrix_to_list(S)
        modified_g_as_list = matrix_to_list(N(G))
        g_as_list = matrix_to_list(G)

        #TODO: add planmatch
        options = self.options(i)

        if self.modified_options[i] is None:
            self.modified_options[i] = modify_options(options, N)
            self.modified_graph[i] = construct_graph(self.modified_options[i])

        planner = PlannerIntersection(self.options_dicts[i], N,self.probabilistic, self.modified_options[i], self.modified_graph[i])

        # We are already at the Goal
        if utils.a_subset_b(start_as_list, g_as_list)[0]:
            return True,[]

        if utils.a_subset_b(start_as_list, modified_g_as_list)[0]:
            return self.hierarchical_plan_v2(S, G, i-1)

        result, plan, num_gaps, overlap = planner.bfs_plan(S, G) #PLAN WITH NEIGHBOURHOODS HERE
        plan_len = len(plan)

        # Plan failed: drop to a lower level
        if not result: 
            print("PLAN FAILED, DROPPING TO LOWER LEVEL")
            return self.hierarchical_plan_v2(S, G, i-1)

        # TO-DO: ADD IS PLAN EFFECTIVE
        if i is not 0:
            num_options = self.num_options(i - 1)
            neighbourhood_sz = self.neighbourhood_sz(i)
            option_sz = self.option_sz(i - 1)
            IPE = IsPlanEffective(option_sz, num_options, neighbourhood_sz, overlap, 0.5)
            if not IPE.is_plan_effective(num_gaps, S, G):
                print("PLAN IS NOT EFFECTIVE, DROPPING TO LOWER LEVEL")
                return self.hierarchical_plan_v2(S, G, i-1)
        #stitching gap at start
        index = 0

        if not utils.a_subset_b(start_as_list, plan[0].initiation_as_list)[0]: 

            sub_plan = self.__stitch_gaps(S,plan[0].I,i)

            plan = sub_plan + plan
            index += 1

        #stitching intermediate gaps
        for x in range(plan_len - 1): 

            previous_option = plan[index]
            next_option = plan[index + 1]

            if not utils.a_subset_b(previous_option.termination_as_list, next_option.initiation_as_list)[0]:

                sub_plan = self.__stitch_gaps(previous_option.beta,next_option.I,i)

                plan = plan[:index+1] + sub_plan + plan[index+1:]

                index += 2

            else:
                index += 1

        #stitching gap at end
        last_option = plan[-1]
        if not utils.a_subset_b(last_option.termination_as_list, g_as_list)[0]: 

            sub_plan = self.__stitch_gaps(last_option.beta,G,i)

            plan.append(sub_plan)
            index += 1

        return True, plan

def execute_plan(plan, start, goal):
    current = start

    if utils.a_subset_b(matrix_to_list(current), matrix_to_list(goal))[0]:
        return current
    for sub in plan: 
        if utils.a_subset_b(matrix_to_list(current), matrix_to_list(goal))[0]:
            return current
        if isinstance(sub, list):
            current = execute_plan(sub, current,goal)
        elif utils.a_subset_b(matrix_to_list(current),sub.initiation_as_list)[0]:
            current = sub.execute_policy_probabilistic(current)
            #current = sub.execute_policy(current)
            print(sub.name)
    return current

def unit_tests():
    hp_planner = Hierarchical_plan()
    arr1 = np.zeros((8, 8))
    arr1[1, 1] = 1 #set start state
    arr2 = np.zeros((8, 8))
    arr2[2, 4] = 1 #set goal state
    correct_plan = ["room_1_quad_1->room_1_quad_2", "1_2_right", "room_1_quad_2->room_1_quad_4", "2_3_right"]
    plan = hp_planner.hierarchical_plan_v2(arr1, arr2, 1) #[i[1].name for i in hp_planner.hierarchical_plan_v2(arr1, arr2, 1)[1]]
    print(execute_plan(plan[1], arr1, arr2))
    if plan == correct_plan:
        print("PASS")
    else:
        print("FAIL")
    arr1 = np.zeros((8, 8))
    arr1[3, 3] = 1 #set start state
    arr2 = np.zeros((8, 8))
    arr2[5, 3] = 1 #set goal state
    correct_plan = ["room_1->room_3", "4_3_down"]
    plan = hp_planner.hierarchical_plan_v2(arr1, arr2, 2) #[i[1].name for i in hp_planner.hierarchical_plan_v2(arr1, arr2, 2)[1]]
    print(execute_plan(plan[1], arr1, arr2))
    if plan == correct_plan:
        print("PASS")
    else:
        print("FAIL")

def flatten_list(l):
    ans = []
    for i in l:
        if isinstance(i, list):
            ans = ans + flatten_list(i)
        else:
            ans.append(i)
    return ans
    
def unit_tests_2(): #check of both hierarchical plan algorithms return identical answers in the deterministic case
    arr1 = np.zeros((8,8))
    hp_planner = Hierarchical_plan()
    tests = [[(1, 1), (7, 7)], [(1, 1), (6, 6)], [(2, 3), (4, 5)], [(6, 4), (3, 1)], [(1, 0), (3, 0)]]
    for i in tests:
        arr1 = np.zeros((8,8))
        arr2 = np.zeros((8,8))
        arr1[i[0][0], i[0][1]] = 1
        arr2[i[1][0], i[1][1]] = 1
        print(arr1)
        plan1 = [i[1] for i in hp_planner.hierarchical_plan_v1(arr1, arr2, 2)[1]]
        print("seperator")
        plan2 = flatten_list(hp_planner.hierarchical_plan_v2(arr1, arr2, 2)[1])
        print([i.name for i in plan1])
        print([i.name for i in plan2])
        if plan1 == plan2:
            print("SUCCESS")
        else:
            print("FAIL")
            print(plan1)
            print(plan2)
            print([i.name for i in plan1])
            print([i.name for i in plan2])





if __name__ == "__main__":
    unit_tests_2()

    arr1 = np.zeros((8,8))
    arr1[0, 0] = 1 #set start state

    arr2 = np.zeros((8, 8))
    arr2[7, 7] = 1 #set goal state

    print("START")
    print(arr1)
    print("GOAL")
    print(arr2)

    print("==============================")
    print ("Deterministic Planning Time")
    hp_planner = Hierarchical_plan()
    start_time = time.time()
    plan = hp_planner.hierarchical_plan_v2(arr1, arr2, 2)
    end_time = time.time()
    print("HERE: ", flatten_list(plan[1]))

    # for o in plan[1]:
    #     print(o[1].name)

    elapsed_time = end_time - start_time


    print(elapsed_time)
    print("==============================")

    print("==============================")
    print ("Deterministic Planning Time 2")
    start_time = time.time()
    plan = hp_planner.hierarchical_plan_v2(arr1, arr2, 2)

    end_time = time.time()

    # for o in plan[1]:
    #     print(o[1].name)

    elapsed_time = end_time - start_time


    print(elapsed_time)
    print("==============================")

    print ("Stochastic Planning Time")

    probabilistic = True

    hp_planner_stochastic = Hierarchical_plan(probabilistic)
    start_time = time.time()
    plan = hp_planner_stochastic.hierarchical_plan_v2(arr1, arr2, 2)
    end_time = time.time()

    elapsed_time = end_time - start_time

    execute_plan(plan[1],arr1,arr2)

    print(elapsed_time)
    print("==============================")

    print ("Stochastic Planning Time 2")

    probabilistic = True

    start_time = time.time()
    plan = hp_planner_stochastic.hierarchical_plan_v2(arr1, arr2, 2)
    end_time = time.time()

    elapsed_time = end_time - start_time

    execute_plan(plan[1],arr1,arr2)

    print(elapsed_time)
    print("==============================")

    print ("Planning With All Options")

    start_time = time.time()

    N = Neighbourhood("naive",0,0,0).N0
    planner = Planner(mdp_2 + mdp_1 + mdp_0, N)
    # #planner = Planner(mdp_2 + mdp_1 + mdp_0, N)
    # planner = Planner(mdp_0, N)
    result, plan, dummy = planner.bfs_plan(arr1, arr2) #PLAN WITH NEIGHBOURHOODS HERE

    end_time = time.time()

    elapsed_time = end_time - start_time

    for o in plan:
        print(o[1].name)

    print(elapsed_time)
    print("==============================")
