import numpy as np
from main import a_subset_b, mdp_1

class Neighbourhood():
    def __init__(self):
        #memoize previously computed neighbourhoods
        self.N1_store = {}
        self.N2_store = {}
    

    def union(self, A, B): #take the union of two sets of states
        N = [[0 for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if A[i][j] or B[i][j]:
                    N[i][j] = 1
        return N

    def f(self, mdp, S): #corresponds to the f function in the proposal
        N = [[0 for _ in range(8)] for _ in range(8)]
        for option in mdp:
            if a_subset_b(option.beta, S):
                N = self.union(N, option.I)
        return N


    def N0(self, S):
        return S #there is no neighbourhood in the base mdp as there is no further stitching

    def N1(self, S): 
        #for the neighbourhood on the 1st level, we only want to add the states that are one primitive action away, 
        #this function does that
        if S in self.N1_store:
            return self.N1_store[S]
        N = [[0 for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                neighbours = [S[i][j], S[i][max(j - 1, 0)], S[max(i - 1, 0)][j], \
                    S[min(i+1, 7)][j], S[i][min(j + 1, 7)]]
                if 1 in neighbours:
                    N[i][j] = 1
        self.N1_store[S] = N
        return N

    def N2(self, S): #neighbourhood for topmost level of abstraction
        if S in self.N2_store:
            return self.N2_store[S]
        S1 = self.N1(S)
        f1 = self.f(mdp_1, S)
        N = self.union(S1, f1)
        self.N2_store[S] = N
        return N



    

        