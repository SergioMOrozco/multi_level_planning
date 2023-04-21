from neighbourhood import Neighbourhood
from utils import matrix_to_list
import numpy as np
import math

class IsPlanEffective():
    def __init__(self, option_len, num_options, neighbourhood_size) -> None:
        self.option_len = option_len
        self.num_options = num_options

        self.neighbourhood_size = neighbourhood_size


    def T(self, gap_sz, option_sz, num_options):
        plan_sz = gap_sz/option_sz
        plan_time = num_options**plan_sz
        return plan_time

    def M(self, S, G): #return the worst case manhattan dist
        S = matrix_to_list(S)
        G = matrix_to_list(G)
        max =  - math.inf
        for i in S:
            for j in G:
                manhattan_dist = abs(i[0] - j[0]) + abs(i[1] - j[1])
                if manhattan_dist > max:
                    max = manhattan_dist
        return max

    def is_plan_effective(self, num_gaps, S, G):
        # print("num_gaps: ", num_gaps)
        # print("options_len: ", self.option_len)
        # print("gap len", self.neighbourhood_size)
        dist = self.M(S, G)
        # print("dist: ", dist)
        # print("num options: ", self.num_options)
        t_i = self.T(self.neighbourhood_size, self.option_len, self.num_options)
        # print(t_i)
        t_n_minus_1 = self.T(dist, self.option_len, self.num_options)
        # print(t_n_minus_1)
        if num_gaps * t_i < t_n_minus_1:
            return True
        return False

