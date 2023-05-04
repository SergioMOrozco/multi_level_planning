import numpy as np
from utils import matrix_to_list
from dimension import dim

class Action():
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction 
        self.name = str(position[0]) + "_" + str(position[1]) + "_" + direction
        # Set I (initiation set), beta (termination set), pi (policy) 
        self._setIBetaPi(position, direction)
        self.initiation_as_list = matrix_to_list(self.I)
        self.termination_as_list = matrix_to_list(self.beta)

    def __copy__(self):
        return type(self)(self.position,self.direction)
    def __str__(self):
        return self.name
    def pickAction(self, state):
        action_number = self.pi[state]
        if action_number == 1:
            action = "left"
        elif action_number == 2:
            action = "up"
        elif action_number == 3:
            action = "right"
        elif action_number == 4:
            action = "down"
        else:
            action = "still"
        # Return action number, used for intra-option model learning
        return action, action_number

    def execute_policy_probabilistic(self,S):
        return self.execute_policy(S)

    def execute_policy(self, S): #starting at position S, returns the state obtained after executing option policy
        #not necessary for primitive actions, included so that they can be handled identically to options in options.py
        pos = np.where(S == 1)
        while self.beta[pos] == 0:
            action = self.pi[pos][0]
            if action == 1:
                x = pos[0][0]
                y = pos[1][0] - 1
            elif action == 2:
                x = pos[0][0] - 1
                y = pos[1][0]
            elif action == 3:
                x = pos[0][0]
                y = pos[1][0] + 1
            elif action == 4:
                x = pos[0][0] + 1
                y = pos[1][0]
            pos = ([x], [y])
        final_state = np.zeros((dim, dim))
        final_state[pos] = 1
        return final_state

    # def list_initiation_states(self): #Split a set of states into a list of stat_result
    #     states = []
    #     for i in range(8):
    #         for j in range(8):
    #             if self.I[i][j] == 1:
    #                 arr = np.zeros((8, 8))
    #                 arr[i][j] = 1
    #                 states.append(arr)
    #     return states
    
    # def list_termination_states(self): #Split a set of states into a list of stat_result
    #     states = []
    #     for i in range(8):
    #         for j in range(8):
    #             if self.beta[i][j] == 1:
    #                 arr = np.zeros((8, 8))
    #                 arr[i][j] = 1
    #                 states.append(arr)
    #     return states


               
    def _setIBetaPi(self, position,direction):
        self.I = np.zeros((dim, dim))
        self.I[position] = 1 # available at start position
        self.beta = np.zeros((dim, dim))
        
        if direction == "left":
            adjusted = (position[0], max(0,position[1] - 1)) # don't move on leftmost positions
            self.beta[adjusted] = 1 # terminates after moving left
            self.pi = np.zeros((dim, dim))

            # check for edge case
            if not adjusted == position:
                self.pi[position] = 1

        if direction == "up":
            adjusted = (max(0,position[0] -1),position[1]) # don't move on upmost positions
            self.beta[adjusted] = 1 # terminates after moving left
            self.pi = np.zeros((dim, dim))

            # check for edge case
            if not adjusted == position:
                self.pi[position] = 2

        if direction == "right":
            adjusted = (position[0], min(dim - 1,position[1] + 1)) # don't move on leftmost positions
            self.beta[adjusted] = 1 # terminates after moving left
            self.pi = np.zeros((dim, dim))

            # check for edge case
            if not adjusted == position:
                self.pi[position] = 3

        if direction == "down":
            adjusted = (min(dim - 1,position[0] + 1),position[1]) # don't move on upmost positions
            self.beta[adjusted] = 1 # terminates after moving left
            self.pi = np.zeros((dim, dim))

            # check for edge case
            if not adjusted == position:
                self.pi[position] = 4

      
    def __str__(self):
        return self.name

if __name__ == "__main__":
    action = Action((6,0), "down")
    print("Initiation Set")
    print(action.I)
    print("Termination Set")
    print(action.beta)
    print("Pi")
    print(action.pi)
    print(action.name)
