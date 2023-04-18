from os import stat_result
import numpy as np

class Option():
    def __init__(self, option, I = None, beta = None, pi = None):
        self.name = option
        # Set I (initiation set), beta (termination set), pi (policy) 
        if I is not None:
            self.I = I
            self.beta = beta
            self.pi = pi
        else:
            self._setIBetaPi()
        
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

    def execute_policy(self, S): #starting at position S, returns the state obtained after executing option policy
        # NOTE: we don't want to actually execute policies while planning, this is just a cheap patch to avoid partitioning the options in main.py by hand
        pos = np.where(S == 1)
        # print("pos: ", pos)
        # print(self.beta)
        #print(self.name)
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
        final_state = np.zeros((8, 8))
        final_state[pos] = 1
        return final_state

    def list_initiation_states(self): #Split a set of states into a list of stat_result
        states = []
        for i in range(8):
            for j in range(8):
                if self.I[i][j] == 1:
                    #print("here")
                    arr = np.zeros((8, 8))
                    arr[i][j] = 1
                    states.append(arr)
        return states

    def list_termination_states(self): #Split a set of states into a list of stat_result
        states = []
        for i in range(8):
            for j in range(8):
                if self.beta[i][j] == 1:
                    arr = np.zeros((8, 8))
                    arr[i][j] = 1
                    states.append(arr)
        return states


               
    def _setIBetaPi(self):
        self.I = np.zeros((8, 8))
        self.beta = np.zeros((8, 8))
        self.pi = np.zeros((8, 8))

        if self.name == "room_2->room_1":
            self.I[0:4, 4:8] = 1 # executable from room 2

            self.beta[0:4, 0:4] = 1 # terminates at room 1

            self.pi[0:4, 4:8] = 1 # go left when in room 2
        
        elif self.name == "room_3->room_1":
            self.I[4:8, 0:4] = 1 # executable from room 3

            self.beta[0:4, 0:4] = 1 # terminates at room 1

            self.pi[4:8, 0:4] = 2 # go up when in room 3 

        elif self.name == "room_1_quad_2->room_1_quad_1":
            self.I[0:2, 2:4] = 1 # include room 1 quad 2

            self.beta[0:2, 0:2] = 1 # terminates at room 1 quad 1

            self.pi[0:2, 2:4] = 1 # go left when in room 1 quad 2

        elif self.name == "room_1_quad_3->room_1_quad_1":
            self.I[2:4, 0:2] = 1 # include room 1 quad 3

            self.beta[0:2, 0:2] = 1 # terminates at room 1 quad 1

            self.pi[2:4, 0:2] = 2 # go up when in room 1 quad 3

        elif self.name == "room_1_quad_1->room_1_quad_2":
            self.I[0:2, 0:2] = 1 # include room 1 quad 1

            self.beta[0:2, 2:4] = 1 # terminates at room 1 quad 2

            self.pi[0:2, 0:2] = 3 # go right when in room 1 quad 1

        elif self.name == "room_1_quad_4->room_1_quad_2":
            self.I[2:4, 2:4] = 1 # include room 1 quad 4

            self.beta[0:2, 2:4] = 1 # terminates at room 1 quad 2

            self.pi[2:4, 2:4] = 2 # go up when in room 1 quad 4

        elif self.name == "room_1_quad_1->room_1_quad_3":
            self.I[0:2, 0:2] = 1 # include room 1 quad 1

            self.beta[2:4, 0:2] = 1 # terminates at room 1 quad 3

            self.pi[0:2, 0:2] = 4 # go down when in room 1 quad 1

        elif self.name == "room_1_quad_4->room_1_quad_3":
            self.I[2:4, 2:4] = 1 # include room 1 quad 4

            self.beta[2:4, 0:2] = 1 # terminates at room 1 quad 3

            self.pi[2:4, 2:4] = 1 # go left when in room 1 quad 4

        elif self.name == "room_1_quad_2->room_1_quad_4":
            self.I[0:2, 2:4] = 1 # include room 1 quad 2 

            self.beta[2:4, 2:4] = 1 # terminates at room 1 quad 4

            self.pi[0:2, 2:4] = 4 # go down when in room 1 quad 2

        elif self.name == "room_1_quad_3->room_1_quad_4":
            self.I[2:4, 0:2] = 1 # include room 1 quad 2  

            self.beta[2:4, 2:4] = 1 # terminates at room 1 quad 4

            self.pi[2:4, 0:2] = 3 # go right when in room 1 quad 3

        elif self.name == "room_1->room_2":
            self.I[0:4, 0:4] = 1 # executable from room 1

            self.beta[0:4, 4:8] = 1 # terminates at room 2

            self.pi[0:4, 0:4] = 3 # go right when in room 1
        
        elif self.name == "room_4->room_2":
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.beta[0:4, 4:8] = 1 # terminates at room 2

            self.pi[4:8, 4:8] = 2 # go up when in room 4 

        elif self.name == "room_2_quad_2->room_2_quad_1":
            self.I[0:2, 6:8] = 1 # executable from room 2 quad 2

            self.beta[0:2, 4:6] = 1 # terminates at room 2 quad 1

            self.pi[0:2, 6:8] = 1 # go left when in room 2 quad 2

        elif self.name == "room_2_quad_3->room_2_quad_1":
            self.I[2:4, 4:6] = 1 # executable from room 2 quad 3 

            self.beta[0:2, 4:6] = 1 # terminates at room 2 quad 1

            self.pi[2:4, 4:6] = 2 # go up when in room 2 quad 3

        elif self.name == "room_2_quad_1->room_2_quad_2":
            self.I[0:2, 4:6] = 1 # executable from room 2 quad 1 

            self.beta[0:2, 6:8] = 1 # terminates at room 2 quad 2

            self.pi[0:2, 4:6] = 3 # go right when in room 2 quad 1

        elif self.name == "room_2_quad_4->room_2_quad_2":
            self.I[2:4, 6:8] = 1 # executable from room 2 quad 4 

            self.beta[0:2, 6:8] = 1 # terminates at room 2 quad 2

            self.pi[2:4, 6:8] = 2 # go up when in room 2 quad 4

        elif self.name == "room_2_quad_1->room_2_quad_3":
            self.I[0:2, 4:6] = 1 # executable from room 2 quad 1 

            self.beta[2:4, 4:6] = 1 # terminates at room 2 quad 3

            self.pi[0:2, 4:6] = 4 # go down when in room 2 quad 1

        elif self.name == "room_2_quad_4->room_2_quad_3":
            self.I[2:4, 6:8] = 1 # executable from room 2 quad 4 

            self.beta[2:4, 4:6] = 1 # terminates at room 2 quad 3

            self.pi[2:4, 6:8] = 1 # go left when in room 2 quad 4

        elif self.name == "room_2_quad_2->room_2_quad_4":
            self.I[0:2, 6:8] = 1 # executable from room 2 quad 2 

            self.beta[2:4, 6:8] = 1 # terminates at room 2 quad 4

            self.pi[0:2, 6:8] = 4 # go down when in room 2 quad 2

        elif self.name == "room_2_quad_3->room_2_quad_4":
            self.I[2:4, 4:6] = 1 # executable from room 2 quad 3 

            self.beta[2:4, 6:8] = 1 # terminates at room 2 quad 4

            self.pi[2:4, 4:6] = 3 # go right when in room 2 quad 3

        elif self.name == "room_1->room_3":
            self.I[0:4, 0:4] = 1 # executable from room 1

            self.beta[4:8, 0:4] = 1 # terminates at room 3

            self.pi[0:4, 0:4] = 4 # go down when in room 1

        elif self.name == "room_2->room_3":
            self.I[0:4, 4:8] = 1 # executable from room 2

            self.beta[4:8, 0:4] = 1 # terminates at room 3

            self.pi[0:4, 4:8] = 4 # go down when in room 2

        elif self.name == "room_3_quad_2->room_3_quad_1":
            self.I[4:6, 2:4] = 1 # executable from room 3 quad 2

            self.beta[4:6, 0:2] = 1 # terminates at room 3 quad 1

            self.pi[4:6, 2:4] = 1 # go left when in room 3 quad 2

        elif self.name == "room_3_quad_3->room_3_quad_1":
            self.I[6:8, 0:2] = 2 # executable from room 3 quad 3

            self.beta[4:6, 0:2] = 1 # terminates at room 3 quad 1

            self.pi[6:8, 0:2] = 2 # go up when in room 3 quad 3

        elif self.name == "room_3_quad_1->room_3_quad_2":
            self.I[4:6, 0:2] = 1 # executable from room 3 quad 1

            self.beta[4:6, 2:4] = 1 # terminates at room 3 quad 2

            self.pi[4:6, 0:2] = 3 # go right when in room 3 quad 1

        elif self.name == "room_3_quad_4->room_3_quad_2":
            self.I[6:8, 2:4] = 1 # executable from room 3 quad 4

            self.beta[4:6, 2:4] = 1 # terminates at room 3 quad 2

            self.pi[6:8, 2:4] = 2 # go up when in room 3 quad 4

        elif self.name == "room_3_quad_1->room_3_quad_3":
            self.I[4:6, 0:2] = 1 # executable from room 3 quad 1

            self.beta[6:8, 0:2] = 1 # terminates at room 3 quad 3

            self.pi[4:6, 0:2] = 4 # go down when in room 3 quad 1

        elif self.name == "room_3_quad_4->room_3_quad_3":
            self.I[6:8, 2:4] = 1 # executable from room 3 quad 4

            self.beta[6:8, 0:2] = 1 # terminates at room 3 quad 3

            self.pi[6:8, 2:4] = 1 # go left when in room 3 quad 4

        elif self.name == "room_3_quad_2->room_3_quad_4":
            self.I[4:6, 2:4] = 1 # executable from room 3 quad 2

            self.beta[6:8, 2:4] = 1 # terminates at room 3 quad 4

            self.pi[4:6, 2:4] = 4 # go down when in room 3 quad 2

        elif self.name == "room_3_quad_3->room_3_quad_4":
            self.I[6:8, 0:2] = 1 # executable from room 3 quad 3

            self.beta[6:8, 2:4] = 1 # terminates at room 3 quad 4

            self.pi[6:8, 0:2] = 3 # go right when in room 3 quad 3

        elif self.name == "room_2->room_4":
            self.I[0:4, 4:8] = 1 # executable from room 2

            self.beta[4:8, 4:8] = 1 # terminates at room 4

            self.pi[0:4, 4:8] = 4 # go down when in room 2

        elif self.name == "room_3->room_4":
            self.I[4:8, 0:4] = 1 # executable from room 3

            self.beta[4:8, 4:8] = 1 # terminates at room 4

            self.pi[4:8, 0:4] = 3 # go right when in room 3

        elif self.name == "room_4_quad_2->room_4_quad_1":
            self.I[4:6, 6:8] = 1 # executable from room 4 quad 2

            self.beta[4:6, 4:6] = 1 # terminates at room 4 quad 1

            self.pi[4:6, 6:8] = 1 # go left when in room 4 quad 2

        elif self.name == "room_4_quad_3->room_4_quad_1":
            self.I[6:8, 4:6] = 1 # executable from room 4 quad 3

            self.beta[4:6, 4:6] = 1 # terminates at room 4 quad 1

            self.pi[6:8, 4:6] = 2 # go up when in room 4 quad 3

        elif self.name == "room_4_quad_1->room_4_quad_2":
            self.I[4:6, 4:6] = 1 # executable from room 4 quad 1

            self.beta[4:6, 6:8] = 1 # terminates at room 4 quad 2

            self.pi[4:6, 4:6] = 3 # go left when in room 4 quad 1

        elif self.name == "room_4_quad_4->room_4_quad_2":
            self.I[6:8, 6:8] = 1 # executable from room 4 quad 4

            self.beta[4:6, 6:8] = 1 # terminates at room 4 quad 2

            self.pi[6:8, 6:8] = 2 # go up when in room 4 quad 4

        elif self.name == "room_4_quad_1->room_4_quad_3":
            self.I[4:6, 4:6] = 1 # executable from room 4 quad 1

            self.beta[6:8, 4:6] = 1 # terminates at room 4 quad 3

            self.pi[4:6, 4:6] = 4 # go down when in room 4 quad 1

        elif self.name == "room_4_quad_4->room_4_quad_3":
            self.I[6:8, 6:8] = 1 # executable from room 4 quad 4

            self.beta[6:8, 4:6] = 1 # terminates at room 4 quad 3

            self.pi[6:8, 6:8] = 1 # go left when in room 4 quad 4

        elif self.name == "room_4_quad_2->room_4_quad_4":
            self.I[4:6, 6:8] = 1 # executable from room 4 quad 2

            self.beta[6:8, 6:8] = 1 # terminates at room 4 quad 4

            self.pi[4:6, 6:8] = 4 # go down when in room 4 quad 2

        elif self.name == "room_4_quad_3->room_4_quad_4":
            self.I[6:8, 4:6] = 1 # executable from room 4 quad 3

            self.beta[6:8, 6:8] = 1 # terminates at room 4 quad 4

            self.pi[6:8, 4:6] = 3 # go right when in room 4 quad 3
        elif self.name == "room_4->room_3":
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.beta[4:8, 0:4] = 1 # terminates at room 3

            self.pi[4:8, 4:8] = 1 # go left when in room 4
        else:
            print("Cannot build " + self.name)
            exit(-1)

    def __str__(self):
        return self.name

if __name__ == "__main__":
    option = Option("room_1->room_2")
    print (option.name)
    print("Initiation Set")
    print(option.I)
    print("Termination Set")
    print(option.beta)
    print("Pi")
    print(option.pi)
    arr = np.zeros((8, 8))
    arr[1, 0] = 1
    print(option.execute_policy(arr))
