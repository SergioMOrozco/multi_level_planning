import numpy as np
from option import Option
from action import Action

# the mdp's 

def union(A, B): #take the union of two sets of states
    N = np.array([[0 for _ in range(8)] for _ in range(8)])
    for i in range(8):
        for j in range(8):
            if A[i][j] or B[i][j]:
                N[i][j] = 1
    return N

def to_tuple(S):
    return tuple(map(tuple, S))

def partition_mdp(mdp): #split the option to obey the subgoal condidion, i.e. all state in initiation state should map to same termination state
    new_mdp = []
    for option in mdp:
        # print(option.name)
        # print(option.beta)
        initiation_states = option.list_initiation_states()
        #initiation_to_termination = {to_tuple(i):option.execute_policy(i) for i in initiation_states}
        initiation_to_termination = {}
        for i in initiation_states:
            # print(i)
            initiation_to_termination[to_tuple(i)] = option.execute_policy(i)
            
        termination_to_initiation = {}
        for i in initiation_to_termination:
            tup = to_tuple(initiation_to_termination[i])
            if tup in termination_to_initiation:
                termination_to_initiation[tup] = union(termination_to_initiation[tup], i)
            else:
                termination_to_initiation[tup] = np.array(i)
        for term_state in termination_to_initiation:
            new_mdp.append(Option(option.name, termination_to_initiation[term_state], np.array(term_state), option.pi))
    return new_mdp



mdp_1 = [
        Option("room_1_quad_1->room_1_quad_2"), Option("room_1_quad_1->room_1_quad_3"),
        Option("room_1_quad_2->room_1_quad_1"), Option("room_1_quad_2->room_1_quad_4"),
        Option("room_1_quad_3->room_1_quad_1"), Option("room_1_quad_3->room_1_quad_4"),
        Option("room_1_quad_4->room_1_quad_2"), Option("room_1_quad_4->room_1_quad_3"),

        Option("room_2_quad_1->room_2_quad_2"), Option("room_2_quad_1->room_2_quad_3"),
        Option("room_2_quad_2->room_2_quad_1"), Option("room_2_quad_2->room_2_quad_4"),
        Option("room_2_quad_3->room_2_quad_1"), Option("room_2_quad_3->room_2_quad_4"),
        Option("room_2_quad_4->room_2_quad_2"), Option("room_2_quad_4->room_2_quad_3"),

        Option("room_3_quad_1->room_3_quad_2"), Option("room_3_quad_1->room_3_quad_3"),
        Option("room_3_quad_2->room_3_quad_1"), Option("room_3_quad_2->room_3_quad_4"),
        Option("room_3_quad_3->room_3_quad_1"), Option("room_3_quad_3->room_3_quad_4"),
        Option("room_3_quad_4->room_3_quad_2"), Option("room_3_quad_4->room_3_quad_3"),

        Option("room_4_quad_1->room_4_quad_2"), Option("room_4_quad_1->room_4_quad_3"),
        Option("room_4_quad_2->room_4_quad_1"), Option("room_4_quad_2->room_4_quad_4"),
        Option("room_4_quad_3->room_4_quad_1"), Option("room_4_quad_3->room_4_quad_4"),
        Option("room_4_quad_4->room_4_quad_2"), Option("room_4_quad_4->room_4_quad_3"),
    ]


mdp_2 = [
        Option("room_1->room_2"), Option("room_1->room_3"),
        Option("room_2->room_1"), Option("room_2->room_4"),
        Option("room_3->room_1"), Option("room_3->room_4"),
        Option("room_4->room_2"), Option("room_4->room_3"),
    ]

mdp_1 = partition_mdp(mdp_1)
mdp_2 = partition_mdp(mdp_2)

mdp_0_placeholder = []

directions = ["left","right","up","down"]
for i in range(8):
    for j in range (8):
        for direction in directions:
            mdp_0_placeholder.append(Action((i,j),direction))

mdp_0 = mdp_0_placeholder

#####################



def a_subset_b(a,b):
    # TODO: This could probably be done better
    for i in range(8):
        for j in range(8):
            if not a[(i,j)] <= b[(i,j)] :
                return False
    return True

def plan_match(start,goal, mdp):
    start_option = None
    goal_option = None
    for option in mdp:
        if a_subset_b(start, option.I):
            start_option = option

        if a_subset_b(option.beta, goal):
            goal_option = option

        if not start_option == None and not goal_option == None:
            # print(start_option.name)
            # print(goal_option.name)
            return True

    return False

def main():
    print("hello")
    print([i.beta for i in mdp_0])

    
    # for option in mdp_2:
    #     print(option.name, option.I, option.beta, sep='\n')
    # # quick example of plan matching with different MDP levels
    # start = np.zeros((8,8))
    # goal = np.zeros((8,8))


    # start[(4,4)] = 1

    # goal[(0,0)] = 1
    # goal[(1,0)] = 1
    # goal[(0,1)] = 1
    # goal[(1,1)] = 1

    # print("Start State")
    # print(start)

    # print("Goal State")
    # print(goal)

    # print ("Plan match found at MDP_0: " + str(plan_match(start,goal,mdp_0)))
    # print ("Plan match found at MDP_1: " + str(plan_match(start,goal,mdp_1)))
    # print ("Plan match found at MDP_2: " + str(plan_match(start,goal,mdp_2)))

if __name__ == "__main__":
    main()
