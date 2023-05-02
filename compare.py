from hiearchical_plan import *
from graph_planner import *

directions = ["left","right","up","down"]
for i in range(8):
    for j in range (8):
        for direction in directions:
            mdp_0_placeholder.append(Action((i,j),direction))

mdp_0 = mdp_0_placeholder

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


graph_planner = GraphPlanner([mdp_0, mdp_1, mdp_2])
graph = graph_planner.build_graph_new()




hp_planner = Hierarchical_plan()




num_test_cases = 10000
list_graph_times = []
list_hp_times = []

for i in range(num_test_cases):
    if i%100 == 0:
        print("Test case: ", i)

    # generate random start and goal states
    start_state = random.randint(0, 63)
    goal_state = random.randint(0, 63)

    # find shortest path using graph planner
    start_time = time.time()
    # if graph_planner.saved_dist[start_state, goal_state] != 0:
    #     print("dist = ", graph_planner.saved_dist[start_state, goal_state])
    # else:
    #     graph_planner.find_shortest_path(start_state, goal_state)
    graph_planner.find_shortest_path(start_state, goal_state)
    end_time = time.time()
    list_graph_times.append(end_time - start_time)


    start_i = start_state // 8
    start_j = start_state % 8

    goal_i = goal_state // 8
    goal_j = goal_state % 8

    arr1 = np.zeros((8,8))
    arr1[start_i, start_j] = 1 #set start state

    arr2 = np.zeros((8, 8))
    arr2[goal_i, goal_j] = 1  # set goal state

    # find shortest path using hierarchical planner
    #plan = hp_planner.hierarchical_plan_v2(arr1, arr2, 2)
    start_time = time.time()
    plan = hp_planner.hierarchical_plan_v2(arr1, arr2, 2)
    end_time = time.time()
    list_hp_times.append(end_time - start_time)


print("Average time for graph planner: ", np.mean(list_graph_times))
print("Average time for hierarchical planner: ", np.mean(list_hp_times))