import numpy as np
from option import Option
from action import Action

# the mdp's 

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
    

    

    # quick example of plan matching with different MDP levels
    start = np.zeros((8,8))
    goal = np.zeros((8,8))


    start[(4,4)] = 1

    goal[(0,0)] = 1
    goal[(1,0)] = 1
    goal[(0,1)] = 1
    goal[(1,1)] = 1

    print("Start State")
    print(start)

    print("Goal State")
    print(goal)

    print ("Plan match found at MDP_0: " + str(plan_match(start,goal,mdp_0)))
    print ("Plan match found at MDP_1: " + str(plan_match(start,goal,mdp_1)))
    print ("Plan match found at MDP_2: " + str(plan_match(start,goal,mdp_2)))

if __name__ == "__main__":
    main()
