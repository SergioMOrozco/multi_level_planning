import numpy as np
from main import a_subset_b
import math
from dimension import *

#implementation of naive neighbourhood
class Neighbourhood():
    def __init__(self, type, mdps):
        #memoize previously computed neighbourhoods
        self.type = type
        self.basic_store = [{} for i in range(num_levels)]
        self.advanced_store = [{} for i in range(num_levels)]
        self.mdps = mdps
        
    

    def union(self, A, B): #take the union of two sets of states
        N = np.array([[0 for _ in range(dim)] for _ in range(dim)])
        for i in range(dim):
            for j in range(dim):
                if A[i][j] or B[i][j]:
                    N[i][j] = 1
        return N

    def f(self, mdp, S): #corresponds to the f function in the proposal
        N = np.copy(S)
        for option in mdp:
            if a_subset_b(option.beta, S):
                N = self.union(N, option.I)
            # for state in option.list_initiation_states():
            #     # if a_subset_b(option.beta, S):
            #     if a_subset_b(option.execute_policy(state), S):
            #         N = self.union(N, state)
        return N


    def N_basic(self, S, i): # i should start from 0
        if i == 0:
            return S
        if S.tobytes() in self.basic_store[i]:
            return self.basic_store[i][S.tobytes()]
        S0 = self.N_basic(S, i - 1)
        f0 = self.f(self.mdps[i - 1], S)
        N = self.union(S0, f0)
        self.basic_store[i][S.tobytes()] = N
        return N

    def N(self, S, i):
        if self.type == "naive":
            return self.N_basic(S, i)
        elif self.type == "advanced":
            if i == 0:
                return S
            hash = S.tobytes()
            if hash in self.advanced_store[i]:
                return self.advanced_store[i][hash]
            #assume all ratios are 2
            #trying out this smaller version of neighbourhood
            S = self.union(self.f(self.mdps[i - 1], S), self.N(S, i - 1))
            S = self.f(self.mdps[i - 1], S)
            self.advanced_store[i][hash] = S
            return S





    # if self.type == "naive":
    #         return self.N2_basic(S)
    #     elif self.type == "advanced":
    #         hash = S.tobytes()
    #         if hash in self.N2_store_advanced:
    #             return self.N2_store_advanced[hash]
    #         ratio = int(self.l2/(2*self.l1))
    #         S = self.union(self.f(mdp_1, S), self.N1(S))
    #         for i in range(ratio):
    #             S = self.f(mdp_1, S)
    #             S = self.union(self.f(mdp_1, S), self.N1(S))
    #         self.N2_store_advanced[hash] = S
    #         return S

    # def N_advanced(self, S, i):

    
    
    # def N1(self, S):
    #     if self.type == "naive":
    #         return self.N1_basic(S)
    #     elif self.type == "advanced":
    #         hash = S.tobytes()
    #         if hash in self.N1_store_advanced:
    #             return self.N1_store_advanced[hash]
    #         #ratio should be tunable like a hyperparameter
    #         ratio = math.ceil(self.l1/self.l0) #made an exception - this definition makes more sense than what is in the proposal for level 1
    #         for i in range(ratio):
    #             S = self.N1_basic(S)
    #         self.N1_store_advanced[hash] = S
    #         return S


    # def N2(self, S):
    #     if self.type == "naive":
    #         return self.N2_basic(S)
    #     elif self.type == "advanced":
    #         hash = S.tobytes()
    #         if hash in self.N2_store_advanced:
    #             return self.N2_store_advanced[hash]
    #         ratio = int(self.l2/(2*self.l1))
    #         S = self.union(self.f(mdp_1, S), self.N1(S))
    #         for i in range(ratio):
    #             S = self.f(mdp_1, S)
    #             S = self.union(self.f(mdp_1, S), self.N1(S))
    #         self.N2_store_advanced[hash] = S
    #         return S





if __name__ == "__main__":
    from main import mdps
    neigh = Neighbourhood("advanced", mdps)

    # neigh = Neighbourhood("advanced", 4, 2, 1)
    arr1 = np.zeros((8, 8))
    arr1[6, 6] = 1
    # print(arr1)
    # print(neigh.f(mdp_0, arr1))
    arr2 = np.zeros((8, 8))
    arr2[0, 1] = 1
    # # print(arr1)
    # # print(arr2)
    print(neigh.N(arr1, 2))
    # # print(neigh.union(arr1, arr2))
    # # print(neigh.N1(arr1))
    # # print("NOW")
    # # print(neigh.N2(arr1))
    # print("testing pending for N2. Make termination conditions of options more accurate, and encorporate the intersection concept")




    

        