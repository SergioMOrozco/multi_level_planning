from hiearchical_plan import *
from planner_naive import PlannerNaive
from utils import construct_graph
from main import mdp_0, all_options
from dimension import dim
from Konidaris_baseline import Konidaris_baseline
import matplotlib.pyplot as plt

def flatten_list(l):
    ans = []
    for i in l:
        if isinstance(i, list):
            ans = ans + flatten_list(i)
        else:
            ans.append(i)
    return ans

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
Kb = Konidaris_baseline()
#Intersection(options_dict, N, False, mdp_0, construct_graph(options_dict, mdp_0, False))

print(3)

num_test_cases = 1000
hp_count = [0, 0, 0, 0]
k_count = [0, 0, 0, 0]

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
    plan = flatten_list(plan[1])
    for option in plan:
        hp_count[option.lvl] += 1
    #print(end_time - start_time)
    

    
    
    start_time = time.time()
    plan = plan = Kb.plan(arr1, arr2)
    end_time = time.time()

    for option in plan:
        k_count[option.lvl] += 1
    #print(end_time - start_time)

    
hp_count = (np.array(hp_count)/np.sum(hp_count)) * 100
k_count = (np.array(k_count)/np.sum(k_count)) * 100


print(hp_count)
print(k_count)

x_labels = [0, 1, 2, 3]
x = np.arange(4)  
width = 0.4  

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, hp_count, width, color='salmon', label='Hierarchical Planner')
rects2 = ax.bar(x + width/2, k_count, width, color='slateblue', label='Konidaris (2015)')


ax.set_ylabel('Percentage of actions belonging to given level of abstraction')
ax.set_xlabel('Level of abstration')
ax.set_title('Distribution of actions chosen in planning by Hierarchical Planner vs Konidaris (2015)')
ax.set_xticks(x)
ax.set_xticklabels(x_labels)
ax.legend()

fig.tight_layout()
plt.show()