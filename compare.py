from hiearchical_plan import *
from planner_naive import PlannerNaive
from utils import construct_graph
from main import mdp_0, all_options
from dimension import dim
from Konidaris_baseline import Konidaris_baseline
import matplotlib.pyplot as plt


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

# graph_planner = GraphPlanner([mdp_0, mdp_1, mdp_2])
# graph = graph_planner.build_graph_new()


# mdp_0 = all_options
print(1)
hp_planner = Hierarchical_plan()
print(2)
def N(S):
    return S
options_dict = {}
#mdp_0 = mdp_0 + mdp_1 + mdp_2
for o in mdp_0:
    options_dict[o.name] = o
options_dict_all = {}
for option in all_options:
    options_dict_all[option.name] = option
naive_planner = PlannerNaive(options_dict, mdp_0, construct_graph(options_dict, mdp_0, False))
naive_planner_all = PlannerNaive(options_dict_all, all_options, construct_graph(options_dict_all, all_options, False))
Kb = Konidaris_baseline()
#Intersection(options_dict, N, False, mdp_0, construct_graph(options_dict, mdp_0, False))

print(3)

num_test_cases = 1000
list_hp_times = []
list_naive_times = []
list_k_times = []
list_naive_all_times = []


list_hp_lengths= []
list_naive_lengths= []
list_k_lengths = []
list_naive_all_lengths = []

count = 0
for i in range(num_test_cases):
    if i%100 == 0:
        print("Test case: ", i)

    # generate random start and goal states
    start_state = random.randint(0, dim ** 2 - 1)
    goal_state = random.randint(0, dim ** 2 - 1)
    if start_state == goal_state:
        continue
    
   


    start_i = start_state // dim
    start_j = start_state % dim

    goal_i = goal_state // dim
    goal_j = goal_state % dim

    if abs(goal_i - start_i) + abs(goal_j - start_j) < 10:
        continue
    count += 1
    arr1 = np.zeros((dim,dim))
    arr1[start_i, start_j] = 1 #set start state

    arr2 = np.zeros((dim, dim))
    arr2[goal_i, goal_j] = 1  # set goal state

    #find shortest path using hierarchical planner
    plan = hp_planner.hierarchical_plan_v2(arr1, arr2, num_levels - 1)
    start_time = time.time()
    plan = hp_planner.hierarchical_plan_v2(arr1, arr2, num_levels - 1)
    end_time = time.time()
    #print(end_time - start_time)

    low_level_plan_length = get_plan_length_hp([start_i,start_j],plan)
    list_hp_lengths.append(low_level_plan_length)

    if i > 10:
        list_hp_times.append(end_time - start_time)



    #find path using mnaive planner

    start_time = time.time()
    plan = naive_planner.bfs_plan(arr1, arr2)
    end_time = time.time()
    #print(end_time - start_time)

    low_level_plan_length = get_plan_length([start_i,start_j],plan)
    list_naive_lengths.append(low_level_plan_length)

    if i > 10:
        list_naive_times.append(end_time - start_time)
    
    start_time = time.time()
    plan = plan = Kb.plan(arr1, arr2)
    end_time = time.time()
    #print(end_time - start_time)

    low_level_plan_length = get_plan_length([start_i,start_j],plan)
    list_k_lengths.append(low_level_plan_length)

    if i > 10:
        list_k_times.append(end_time - start_time)

    start_time = time.time()
    plan = naive_planner_all.bfs_plan(arr1, arr2)
    end_time = time.time()
    #print(end_time - start_time)

    low_level_plan_length = get_plan_length([start_i,start_j],plan)
    list_naive_all_lengths.append(low_level_plan_length)

    if i > 10:
        list_naive_all_times.append(end_time - start_time)
    

times = [np.mean(list_hp_times), np.mean(list_naive_times), np.mean(list_k_times), np.mean(list_naive_all_times)]
times_var = np.array([np.std(list_hp_times), np.std(list_naive_times), np.std(list_k_times), np.std(list_naive_all_times)])/np.sqrt(990)
# print("Average time for graph planner: ", np.mean(list_graph_times))
# print("Average time for hierarchical planner: ", np.mean(list_hp_times))
# print("Average time for naive planner: ", np.mean(list_naive_times))

# print("Average length for graph planner: ", np.mean(list_graph_lengths))
# print("Average length for hierarchical planner: ", np.mean(list_hp_lengths))
# print("Average length for naive planner: ", np.mean(list_naive_lengths))

lengths = [np.mean(list_hp_lengths), np.mean(list_naive_lengths), np.mean(list_k_lengths), np.mean(list_naive_all_lengths)]
lengths_var = np.array([np.std(list_hp_lengths), np.std(list_naive_lengths), np.std(list_k_lengths), np.std(list_naive_all_lengths)])/np.sqrt(count)
print(count)
print(times)
print(times_var)
print(lengths)
print(lengths_var)
x_labels = ["Hierarchical Plan", "Base options", "Konidaris (2015)", "All options"]
x = np.arange(len(x_labels))  
width = 0.5  
fig, ax = plt.subplots()
rects1 = ax.bar(x , times, width, color='salmon',  yerr=times_var)
#rects2 = ax.bar(x + width/2, hp_mean_list, width, color='slateblue', label='Hierarchical Planner', yerr=hp_sem_list)


ax.set_ylabel('Time (s)')
ax.set_xlabel('Algorithm Used')
ax.set_title('Comparison of planning time for different algorithms (long tasks)')
ax.set_xticks(x)
ax.set_xticklabels(x_labels)

fig.tight_layout()
plt.show()
fig, ax = plt.subplots()
rects1 = ax.bar(x , lengths, width, color='salmon',  yerr=lengths_var)
#rects2 = ax.bar(x + width/2, hp_mean_list, width, color='slateblue', label='Hierarchical Planner', yerr=hp_sem_list)


ax.set_ylabel('Time (s)')
ax.set_xlabel('Algorithm Used')
ax.set_title('Comparison of plan length for different algorithms (long tasks)')
ax.set_xticks(x)
ax.set_xticklabels(x_labels)

fig.tight_layout()
plt.show()