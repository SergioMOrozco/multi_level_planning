from hiearchical_plan import *
from graph_planner import *
from planner_naive import PlannerNaive
from utils import construct_graph
from main import mdp_0, mdp_1, mdp_2

directions = ["left","right","up","down"]
mdp_0_placeholder = []
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

def get_plan_length_hp(start_state,plan):
    return get_plan_length(start_state,plan[1])

def get_plan_length(start_state,plan):

    start_i = start_state[0]
    start_j = start_state[1]

    distance = 0
    for option in plan:
        goal_i = option.termination_as_list[0][0]
        goal_j = option.termination_as_list[0][1]

        distance += abs(start_i - goal_i) + abs(start_j - goal_j)

        start_i = goal_i
        start_j = goal_j

    return distance

graph_planner = GraphPlanner([mdp_0, mdp_1, mdp_2])
graph = graph_planner.build_graph_new()




hp_planner = Hierarchical_plan()
def N(S):
    return S
options_dict = {}
mdp_0 = mdp_0 + mdp_1 + mdp_2
for o in mdp_0:
    options_dict[o.name] = o
naive_planner = PlannerNaive(options_dict, mdp_0, construct_graph(options_dict, mdp_0, False))

#Intersection(options_dict, N, False, mdp_0, construct_graph(options_dict, mdp_0, False))



num_test_cases = 64
list_graph_times = []
list_hp_times = []
list_naive_times = []

list_graph_lengths= []
list_hp_lengths= []
list_naive_lengths= []

for i in range(num_test_cases):
    if i%100 == 0:
        print("Test case: ", i)

    # generate random start and goal states
    start_state = random.randint(0, 63)
    goal_state = random.randint(0, 63)
    #goal_state = random.randint(63, 63)

    # find shortest path using graph planner
    start_time = time.time()
    # if graph_planner.saved_dist[start_state, goal_state] != 0:
    #     print("dist = ", graph_planner.saved_dist[start_state, goal_state])
    # else:
    #     graph_planner.find_shortest_path(start_state, goal_state)
    _,low_level_plan_length = graph_planner.find_shortest_path(start_state, goal_state)
    print(low_level_plan_length)
    end_time = time.time()
    list_graph_lengths.append(low_level_plan_length)
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
    plan = hp_planner.hierarchical_plan_v2(arr1, arr2, 2)
    start_time = time.time()
    plan = hp_planner.hierarchical_plan_v2(arr1, arr2, 2)
    end_time = time.time()
    print(end_time - start_time)

    low_level_plan_length = get_plan_length_hp([start_i,start_j],plan)
    list_hp_lengths.append(low_level_plan_length)

    if i > 10:
        list_hp_times.append(end_time - start_time)



    #find path using mnaive planner

    start_time = time.time()
    plan = naive_planner.bfs_plan(arr1, arr2)
    end_time = time.time()
    print(end_time - start_time)

    low_level_plan_length = get_plan_length([start_i,start_j],plan)
    list_naive_lengths.append(low_level_plan_length)

    if i > 10:
        list_naive_times.append(end_time - start_time)


print("Average time for graph planner: ", np.mean(list_graph_times))
print("Average time for hierarchical planner: ", np.mean(list_hp_times))
print("Average time for naive planner: ", np.mean(list_naive_times))

print("Average length for graph planner: ", np.mean(list_graph_lengths))
print("Average length for hierarchical planner: ", np.mean(list_hp_lengths))
print("Average length for naive planner: ", np.mean(list_naive_lengths))
