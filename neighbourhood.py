import numpy as np
from main import a_subset_b, mdp_1, mdp_0
import math

#implementation of naive neighbourhood
class Neighbourhood():
    def __init__(self, type, l2 = 4,  l1 = 2, l0 = 1):
        #memoize previously computed neighbourhoods
        self.N1_store = {}
        self.N2_store = {}
        self.N1_store_advanced = {}
        self.N2_store_advanced = {}
        self.type = type
        self.l0 = l0
        self.l1 = l1
        self.l2 = l2
        if self.type == "naive":
            self.N0_sz = 0
            self.N1_sz = l0
            self.N2_sz = l1
        else:
            self.N0_sz = 0
            self.N1_sz = l1
            self.N2_sz = l2
    

    def union(self, A, B): #take the union of two sets of states
        N = np.array([[0 for _ in range(8)] for _ in range(8)])
        for i in range(8):
            for j in range(8):
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


    def N0(self, S):
        return S #there is no neighbourhood in the base mdp as there is no further stitching

    def N1_basic(self, S): 
        #for the neighbourhood on the 1st level, we only want to add the states that are one primitive action away, 
        #THE COMMENTED OUT CODE RUNS FASTER, BUT IS NOT AS GENERALISABLE
        # if S.tobytes() in self.N1_store:
        #     return self.N1_store[S.tobytes()]
        # N = np.array([[0 for _ in range(8)] for _ in range(8)])
        # for i in range(8):
        #     for j in range(8):
        #         neighbours = [S[i][j], S[i][max(j - 1, 0)], S[max(i - 1, 0)][j], \
        #             S[min(i+1, 7)][j], S[i][min(j + 1, 7)]]
        #         if 1 in neighbours:
        #             N[i][j] = 1
        # self.N1_store[S.tobytes()] = N
        if S.tobytes() in self.N1_store:
            return self.N1_store[S.tobytes()]
        S0 = S
        f0 = self.f(mdp_0, S)
        N = self.union(S0, f0)
        self.N1_store[S.tobytes()] = N
        return N
    def N1(self, S):
        if self.type == "naive":
            return self.N1_basic(S)
        elif self.type == "advanced":
            hash = S.tobytes()
            if hash in self.N1_store_advanced:
                return self.N1_store_advanced[hash]
            #ratio should be tunable like a hyperparameter
            ratio = math.ceil(self.l1/self.l0) #made an exception - this definition makes more sense than what is in the proposal for level 1
            for i in range(ratio):
                S = self.N1_basic(S)
            self.N1_store_advanced[hash] = S
            return S

    def N2_basic(self, S): #neighbourhood for topmost level of abstraction
        if S.tobytes() in self.N2_store:
            return self.N2_store[S.tobytes()]
        S1 = self.N1_basic(S)
        f1 = self.f(mdp_1, S)
        N = self.union(S1, f1) #from definition in the handout
        self.N2_store[S.tobytes()] = N
        return N

    def N2(self, S):
        if self.type == "naive":
            return self.N2_basic(S)
        elif self.type == "advanced":
            hash = S.tobytes()
            if hash in self.N2_store_advanced:
                return self.N2_store_advanced[hash]
            ratio = int(self.l2/(2*self.l1))
            S = self.union(self.f(mdp_1, S), self.N1(S))
            for i in range(ratio):
                S = self.f(mdp_1, S)
                S = self.union(self.f(mdp_1, S), self.N1(S))
            self.N2_store_advanced[hash] = S
            return S





if __name__ == "__main__":
    neigh = Neighbourhood("advanced", 4, 2, 1)
    arr1 = np.zeros((8, 8))
    arr1[6, 6] = 1
    print(arr1)
    print(neigh.f(mdp_0, arr1))
    # arr2 = np.zeros((8, 8))
    # arr2[0, 1] = 1
    # print(arr1)
    # print(arr2)
    # print(neigh.union(arr1, arr2))
    # print(neigh.N1(arr1))
    # print("NOW")
    # print(neigh.N2(arr1))
    print("testing pending for N2. Make termination conditions of options more accurate, and encorporate the intersection concept")




    

        