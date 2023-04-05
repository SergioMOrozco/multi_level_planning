import numpy as np
from main import a_subset_b, mdp_1

class Neighbourhood():
    def __init__(self):
        #memoize previously computed neighbourhoods
        self.N1_store = {}
        self.N2_store = {}
    

    def union(self, A, B): #take the union of two sets of states
        N = np.array([[0 for _ in range(8)] for _ in range(8)])
        for i in range(8):
            for j in range(8):
                if A[i][j] or B[i][j]:
                    N[i][j] = 1
        return N

    def f(self, mdp, S): #corresponds to the f function in the proposal
        N = [[0 for _ in range(8)] for _ in range(8)]
        for option in mdp:
            for state in option.list_initiation_states():
                # if a_subset_b(option.beta, S):
                if a_subset_b(option.execute_policy(state), S):
                    N = self.union(N, state)
        return N


    def N0(self, S):
        return S #there is no neighbourhood in the base mdp as there is no further stitching

    def N1(self, S): 
        #for the neighbourhood on the 1st level, we only want to add the states that are one primitive action away, 
        #this function does that
        if S.tobytes() in self.N1_store:
            return self.N1_store[S.tobytes()]
        N = np.array([[0 for _ in range(8)] for _ in range(8)])
        for i in range(8):
            for j in range(8):
                neighbours = [S[i][j], S[i][max(j - 1, 0)], S[max(i - 1, 0)][j], \
                    S[min(i+1, 7)][j], S[i][min(j + 1, 7)]]
                if 1 in neighbours:
                    N[i][j] = 1
        self.N1_store[S.tobytes()] = N
        return N

    def N2(self, S): #neighbourhood for topmost level of abstraction
        if S.tobytes() in self.N2_store:
            return self.N2_store[S.tobytes()]
        S1 = self.N1(S)
        f1 = self.f(mdp_1, S)
        N = self.union(S1, f1)
        self.N2_store[S.tobytes()] = N
        return N

if __name__ == "__main__":
    neigh = Neighbourhood()
    arr1 = np.zeros((8, 8))
    arr1[1, 1] = 1
    arr2 = np.zeros((8, 8))
    arr2[0, 1] = 1
    print(arr1)
    print(arr2)
    print(neigh.union(arr1, arr2))
    print(neigh.N1(arr1))
    print("NOW")
    print(neigh.N2(arr1))
    print("testing pending for N2. Make termination conditions of options more accurate, and encorporate the intersection concept")




    

        