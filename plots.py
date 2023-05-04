from hiearchical_plan import *
# from graph_planner import *
import matplotlib.pyplot as plt
from planner_naive import PlannerNaive
from utils import construct_graph
from main import partition_mdp

mdp_0_placeholder = []

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

num_tests = 10000
hp_times = []
plan_match_times = []
base_naive_times = []
mixed_naive_times = []


# hp_planner = Hierarchical_plan()
# def N(S):
#     return S
# options_dict_base = {}
# options_dict_x = {}
# mdp_x = mdp_0 + mdp_1 + mdp_2
# for o in mdp_0:
#     options_dict_base[o.name] = o
# for o in mdp_x:
#     options_dict_x[o.name] = o
# naive_planner_base = PlannerNaive(options_dict_base, mdp_0, construct_graph(options_dict_base, mdp_0, False))
# naive_planner_x = PlannerNaive(options_dict_x, mdp_x, construct_graph(options_dict_x, mdp_x, False))

hp_planner = Hierarchical_plan()
def N(S):
    return S
options_dict = {}
# mdp_0 = mdp_0 + mdp_1 + mdp_2
for o in mdp_0:
    options_dict[o.name] = o
naive_planner = PlannerNaive(options_dict, mdp_0, construct_graph(options_dict, mdp_0, False))


# for i in range(num_tests):
#     #print(i)
#     start_state = random.randint(0, 63)
#     goal_state = random.randint(0, 63)
#     start_i = start_state // 8
#     start_j = start_state % 8

#     goal_i = goal_state // 8
#     goal_j = goal_state % 8

#     arr1 = np.zeros((8,8))
#     arr1[start_i, start_j] = 1

#     arr2 = np.zeros((8, 8))
#     arr2[goal_i, goal_j] = 1 
#     hp_planner.hierarchical_plan_v2(arr1, arr2, 2)
#     start_time = time.time()
#     plan = hp_planner.hierarchical_plan_v2(arr1, arr2, 2)
#     end_time = time.time()
#     if i > 1000:
#         hp_times.append(end_time - start_time)

#     start_time = time.time()
#     plan = naive_planner.bfs_plan(arr1, arr2)
#     end_time = time.time()
#     if i > 1000:
#         base_naive_times.append(end_time - start_time)

    # start_time = time.time()
    # plan = naive_planner_x.bfs_plan(arr1, arr2)
    # end_time = time.time()
    # if i > 1000:
    #     mixed_naive_times.append(end_time - start_time)



# mean_list = [np.mean(hp_times), np.mean(base_naive_times), np.mean(mixed_naive_times)]
# print(mean_list)
# sem_list = [np.std(hp_times),np.std(base_naive_times), np.std(mixed_naive_times)]

num_test_cases = 10000
list_graph_times = []
list_hp_times = []
list_naive_times = []

for i in range(num_test_cases):
    print("Test case: ", i)

    # generate random start and goal states
    start_state = random.randint(0, 63)
    goal_state = random.randint(0, 63)

    # find shortest path using graph planner


    start_i = start_state // 8
    start_j = start_state % 8

    goal_i = goal_state // 8
    goal_j = goal_state % 8
    if abs(goal_i - start_i) + abs(goal_j - start_j) < 10:
        continue
    arr1 = np.zeros((8,8))
    arr1[start_i, start_j] = 1 #set start state

    arr2 = np.zeros((8, 8))
    arr2[goal_i, goal_j] = 1  # set goal state

    # find shortest path using hierarchical planner
    plan = hp_planner.hierarchical_plan_v2(arr1, arr2, 2)
    start_time = time.time()
    plan = hp_planner.hierarchical_plan_v2(arr1, arr2, 2)
    end_time = time.time()

    list_hp_times.append(end_time - start_time)



    #find path using mnaive planner

    start_time = time.time()
    plan = naive_planner.bfs_plan(arr1, arr2)
    end_time = time.time()

    list_naive_times.append(end_time - start_time)


print("Average time for graph planner: ", np.mean(list_graph_times))
print("Average time for hierarchical planner: ", np.mean(list_hp_times))
print("Average time for naive planner: ", np.mean(list_naive_times))

