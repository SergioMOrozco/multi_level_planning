import numpy as np

class Option():
    def __init__(self, option):
        self.name = option
        # Set I (initiation set), beta (termination set), pi (policy) 
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
               
    def _setIBetaPi(self):
        self.I = np.zeros((8, 8))
        self.beta = np.zeros((8, 8))
        self.pi = np.zeros((8, 8))
        
        if self.name == "go_to_room_1":
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.beta[0:4, 0:4] = 1 # terminates at room 1

            self.pi[0:4, 4:8] = 1 # go left when in room 2
            self.pi[4:8, 0:4] = 2 # go up when in room 3 
            self.pi[4:8, 4:8] = 1 # go left when in room 4 

        elif self.name == "go_to_room_1_quad_1":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[0:2,0:2] = 0 # exclude room 1 quad 1

            self.beta[0:2, 0:2] = 1 # terminates at room 1 quad 1

            self.pi[0:2, 2:4] = 1 # go left when in room 1 quad 2
            self.pi[2:4, 0:2] = 2 # go up when in room 1 quad 3
            self.pi[2:4, 2:4] = 2 # go up when in room 1 quad 4
            self.pi[0:4, 4:8] = 1 # go left when in room 2
            self.pi[4:8, 0:4] = 2 # go up when in room 3 
            self.pi[4:8, 4:8] = 1 # go left when in room 4 

        elif self.name == "go_to_room_1_quad_2":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[0:2,2:4] = 0 # exclude room 1 quad 2

            self.beta[0:2, 2:4] = 1 # terminates at room 1 quad 2

            self.pi[0:2, 0:2] = 3 # go right when in room 1 quad 1
            self.pi[2:4, 0:2] = 2 # go up when in room 1 quad 3
            self.pi[2:4, 2:4] = 2 # go up when in room 1 quad 4
            self.pi[0:4, 4:8] = 1 # go left when in room 2
            self.pi[4:8, 0:4] = 2 # go up when in room 3 
            self.pi[4:8, 4:8] = 1 # go left when in room 4 

        elif self.name == "go_to_room_1_quad_3":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[2:4,0:2] = 0 # exclude room 1 quad 3

            self.beta[2:4, 0:2] = 1 # terminates at room 1 quad 3

            self.pi[0:2, 0:2] = 4 # go down when in room 1 quad 1
            self.pi[0:2, 2:4] = 4 # go down when in room 1 quad 2
            self.pi[2:4, 2:4] = 1 # go left when in room 1 quad 4
            self.pi[0:4, 4:8] = 1 # go left when in room 2
            self.pi[4:8, 0:4] = 2 # go up when in room 3 
            self.pi[4:8, 4:8] = 1 # go left when in room 4 

        elif self.name == "go_to_room_1_quad_4":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[2:4,2:4] = 0 # exclude room 1 quad 4

            self.beta[2:4, 2:4] = 1 # terminates at room 1 quad 4

            self.pi[0:2, 0:2] = 4 # go down when in room 1 quad 1
            self.pi[0:2, 2:4] = 4 # go down when in room 1 quad 2
            self.pi[2:4, 0:2] = 3 # go right when in room 1 quad 3
            self.pi[0:4, 4:8] = 1 # go left when in room 2
            self.pi[4:8, 0:4] = 2 # go up when in room 3 
            self.pi[4:8, 4:8] = 1 # go left when in room 4 

        elif self.name == "go_to_room_2":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.beta[0:4, 4:8] = 1 # terminates at room 2

            self.pi[0:4, 0:4] = 3 # go right when in room 1
            self.pi[4:8, 0:4] = 3 # go right when in room 3 
            self.pi[4:8, 4:8] = 2 # go up when in room 4 

        elif self.name == "go_to_room_2_quad_1":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[0:2,4:6] = 0 # exclude room 2 quad 1

            self.beta[0:2, 4:6] = 1 # terminates at room 2 quad 1

            self.pi[0:2, 6:8] = 1 # go left when in room 2 quad 2
            self.pi[2:4, 4:6] = 2 # go up when in room 2 quad 3
            self.pi[2:4, 6:8] = 2 # go up when in room 2 quad 4
            self.pi[0:4, 0:4] = 3 # go right when in room 1
            self.pi[4:8, 0:4] = 2 # go up when in room 3 
            self.pi[4:8, 4:8] = 2 # go up when in room 4 

        elif self.name == "go_to_room_2_quad_2":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[0:2,6:8] = 0 # exclude room 2 quad 2

            self.beta[0:2, 6:8] = 1 # terminates at room 2 quad 2

            self.pi[0:2, 4:6] = 3 # go right when in room 2 quad 1
            self.pi[2:4, 4:6] = 2 # go up when in room 2 quad 3
            self.pi[2:4, 6:8] = 2 # go up when in room 2 quad 4
            self.pi[0:4, 0:4] = 3 # go right when in room 1
            self.pi[4:8, 0:4] = 2 # go up when in room 3 
            self.pi[4:8, 4:8] = 2 # go up when in room 4 

        elif self.name == "go_to_room_2_quad_3":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[2:4,4:6] = 0 # exclude room 2 quad 3

            self.beta[2:4, 4:6] = 1 # terminates at room 2 quad 3

            self.pi[0:2, 4:6] = 4 # go down when in room 2 quad 1
            self.pi[0:2, 6:8] = 4 # go down when in room 2 quad 2
            self.pi[2:4, 6:8] = 1 # go left when in room 2 quad 4
            self.pi[0:4, 0:4] = 3 # go right when in room 1
            self.pi[4:8, 0:4] = 2 # go up when in room 3 
            self.pi[4:8, 4:8] = 2 # go up when in room 4 

        elif self.name == "go_to_room_2_quad_4":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[2:4,6:8] = 0 # exclude room 2 quad 4

            self.beta[2:4, 6:8] = 1 # terminates at room 2 quad 4

            self.pi[0:2, 4:6] = 4 # go down when in room 2 quad 1
            self.pi[0:2, 6:8] = 4 # go down when in room 2 quad 2
            self.pi[2:4, 4:6] = 3 # go right when in room 2 quad 3
            self.pi[0:4, 0:4] = 3 # go right when in room 1
            self.pi[4:8, 0:4] = 2 # go up when in room 3 
            self.pi[4:8, 4:8] = 2 # go up when in room 4 

        elif self.name == "go_to_room_3":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.beta[4:8, 0:4] = 1 # terminates at room 3

            self.pi[0:4, 0:4] = 4 # go down when in room 1
            self.pi[0:4, 4:8] = 4 # go down when in room 2
            self.pi[4:8, 4:8] = 1 # go left when in room 4 

        elif self.name == "go_to_room_3_quad_1":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[4:6,0:2] = 0 # exclude room 3 quad 1

            self.beta[4:6, 0:2] = 1 # terminates at room 3 quad 1

            self.pi[4:6, 2:4] = 1 # go left when in room 3 quad 2
            self.pi[6:8, 0:2] = 2 # go up when in room 3 quad 3
            self.pi[6:8, 2:4] = 2 # go up when in room 3 quad 4
            self.pi[0:4, 0:4] = 4 # go down when in room 1
            self.pi[0:4, 4:8] = 4 # go down when in room 2
            self.pi[4:8, 4:8] = 1 # go left when in room 4 

        elif self.name == "go_to_room_3_quad_2":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[4:6,2:4] = 0 # exclude room 3 quad 2

            self.beta[4:6, 2:4] = 1 # terminates at room 3 quad 2

            self.pi[4:6, 0:2] = 3 # go right when in room 3 quad 1
            self.pi[6:8, 0:2] = 2 # go up when in room 3 quad 3
            self.pi[6:8, 2:4] = 2 # go up when in room 3 quad 4
            self.pi[0:4, 0:4] = 4 # go down when in room 1
            self.pi[0:4, 4:8] = 4 # go down when in room 2
            self.pi[4:8, 4:8] = 1 # go left when in room 4 

        elif self.name == "go_to_room_3_quad_3":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[6:8,0:2] = 0 # exclude room 3 quad 3

            self.beta[6:8, 0:2] = 1 # terminates at room 3 quad 3

            self.pi[4:6, 0:2] = 4 # go down when in room 3 quad 1
            self.pi[4:6, 2:4] = 4 # go down when in room 3 quad 2
            self.pi[6:8, 2:4] = 1 # go left when in room 3 quad 4
            self.pi[0:4, 0:4] = 4 # go down when in room 1
            self.pi[0:4, 4:8] = 4 # go down when in room 2
            self.pi[4:8, 4:8] = 1 # go left when in room 4 

        elif self.name == "go_to_room_3_quad_4":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[6:8,2:4] = 0 # exclude room 3 quad 4

            self.beta[6:8, 2:4] = 1 # terminates at room 3 quad 3

            self.pi[4:6, 0:2] = 4 # go down when in room 3 quad 1
            self.pi[4:6, 2:4] = 4 # go down when in room 3 quad 2
            self.pi[6:8, 0:2] = 3 # go right when in room 3 quad 3
            self.pi[0:4, 0:4] = 4 # go down when in room 1
            self.pi[0:4, 4:8] = 4 # go down when in room 2
            self.pi[4:8, 4:8] = 1 # go left when in room 4 

        elif self.name == "go_to_room_4":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3

            self.beta[4:8, 4:8] = 1 # terminates at room 3

            self.pi[0:4, 0:4] = 3 # go right when in room 1
            self.pi[0:4, 4:8] = 4 # go down when in room 2
            self.pi[4:8, 0:4] = 3 # go right when in room 3

        elif self.name == "go_to_room_4_quad_1":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[4:6,4:6] = 0 # exclude room 4 quad 1

            self.beta[4:6, 4:6] = 1 # terminates at room 4 quad 1

            self.pi[4:6, 6:8] = 1 # go left when in room 4 quad 2
            self.pi[6:8, 4:6] = 2 # go up when in room 4 quad 3
            self.pi[6:8, 6:8] = 2 # go up when in room 4 quad 4
            self.pi[0:4, 0:4] = 4 # go down when in room 1
            self.pi[0:4, 4:8] = 4 # go down when in room 2
            self.pi[4:8, 0:4] = 3 # go right when in room 3

        elif self.name == "go_to_room_4_quad_2":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[4:6,6:8] = 0 # exclude room 4 quad 2

            self.beta[4:6, 6:8] = 1 # terminates at room 4 quad 2

            self.pi[4:6, 4:6] = 3 # go left when in room 4 quad 1
            self.pi[6:8, 4:6] = 2 # go up when in room 4 quad 3
            self.pi[6:8, 6:8] = 2 # go up when in room 4 quad 4
            self.pi[0:4, 0:4] = 4 # go down when in room 1
            self.pi[0:4, 4:8] = 4 # go down when in room 2
            self.pi[4:8, 0:4] = 3 # go right when in room 3

        elif self.name == "go_to_room_4_quad_3":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[6:8,4:6] = 0 # exclude room 4 quad 3

            self.beta[6:8, 4:6] = 1 # terminates at room 4 quad 3

            self.pi[4:6, 4:6] = 4 # go down when in room 4 quad 1
            self.pi[4:6, 6:8] = 4 # go down when in room 4 quad 2
            self.pi[6:8, 6:8] = 1 # go left when in room 4 quad 4
            self.pi[0:4, 0:4] = 4 # go down when in room 1
            self.pi[0:4, 4:8] = 4 # go down when in room 2
            self.pi[4:8, 0:4] = 3 # go right when in room 3

        elif self.name == "go_to_room_4_quad_4":
            self.I[0:4, 0:4] = 1 # executable from room 1
            self.I[0:4, 4:8] = 1 # executable from room 2
            self.I[4:8, 0:4] = 1 # executable from room 3
            self.I[4:8, 4:8] = 1 # executable from room 4

            self.I[6:8,6:8] = 0 # exclude room 4 quad 4

            self.beta[6:8, 6:8] = 1 # terminates at room 4 quad 4

            self.pi[4:6, 4:6] = 4 # go down when in room 4 quad 1
            self.pi[4:6, 6:8] = 4 # go down when in room 4 quad 2
            self.pi[6:8, 4:6] = 3 # go right when in room 4 quad 3
            self.pi[0:4, 0:4] = 4 # go down when in room 1
            self.pi[0:4, 4:8] = 4 # go down when in room 2
            self.pi[4:8, 0:4] = 3 # go right when in room 3

    def __str__(self):
        return self.name

if __name__ == "__main__":
    option = Option("down")
    print("Initiation Set")
    print(option.I)
    print("Termination Set")
    print(option.beta)
    print("Pi")
    print(option.pi)
