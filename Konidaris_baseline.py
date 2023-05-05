from hiearchical_plan import *
from planner_naive import PlannerNaive
from utils import construct_graph
from main import mdps
from dimension import *


class Konidaris_baseline():
    def __init__(self):
        self.options_dict = [{} for i in range(num_levels)]
        for i in range(num_levels):
            for o in mdps[i]:
                self.options_dict[i][o.name] = o   
        self.planners = [PlannerNaive(self.options_dict[i], mdps[i], construct_graph(self.options_dict[i], mdps[i], False)) for i in range(num_levels)]

    def plan(self, S, G):
        for i in range(num_levels - 1, -1, -1):
            plan = self.planners[i].bfs_plan(S, G)
            if plan != []:
                return plan
            print("dropping")
        return []


if __name__ == "__main__":
    planner = Konidaris_baseline()
    arr1 = np.zeros((dim,dim))
    arr1[0, 0] = 1 #set start state
    arr2 = np.zeros((dim, dim))
    arr2[0, 8] = 1  # set goal state
    print([i.name for i in planner.plan(arr1, arr2)])


