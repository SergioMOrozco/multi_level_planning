import numpy as np

class Action():
    def __init__(self, position, direction):
        self.name = str(position[0]) + "_" + str(position[1]) + "_" + direction
        # Set I (initiation set), beta (termination set), pi (policy) 
        self._setIBetaPi(position, direction)
        
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
               
    def _setIBetaPi(self, position,direction):
        self.I = np.zeros((8, 8))
        self.I[position] = 1 # available at start position
        self.beta = np.zeros((8, 8))
        
        if direction == "left":
            adjusted = (position[0], max(0,position[1] - 1)) # don't move on leftmost positions
            self.beta[adjusted] = 1 # terminates after moving left
            self.pi = np.zeros((8, 8))

            # check for edge case
            if not adjusted == position:
                self.pi[position] = 1

        if direction == "up":
            adjusted = (max(0,position[0] -1),position[1]) # don't move on upmost positions
            self.beta[adjusted] = 1 # terminates after moving left
            self.pi = np.zeros((8, 8))

            # check for edge case
            if not adjusted == position:
                self.pi[position] = 2

        if direction == "right":
            adjusted = (position[0], min(7,position[1] + 1)) # don't move on leftmost positions
            self.beta[adjusted] = 1 # terminates after moving left
            self.pi = np.zeros((8, 8))

            # check for edge case
            if not adjusted == position:
                self.pi[position] = 3

        if direction == "down":
            adjusted = (min(7,position[0] + 1),position[1]) # don't move on upmost positions
            self.beta[adjusted] = 1 # terminates after moving left
            self.pi = np.zeros((8, 8))

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
