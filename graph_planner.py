from main import *
import queue
import numpy as np
from neighbourhood import Neighbourhood
import math
from collections import defaultdict
import sys, time

class GraphPlanner():
    def __init__(self, mdps):
        self.mdps = mdps
        self.graph = None
    
    # build a graph of the options and their initiation states
    def build_graph(self):
        # create an empty adjacency list
        graph = np.zeros((64, 64))

        cost_ind = 1

        # iterate over all the mdps
        for mdp in self.mdps:
            mdp_cost = cost_ind**2

            # iterate over all the options
            for option in mdp:

                # Q: how to represent a weighted graph? 
                # iterate over all the initiation states
                for state in option.list_initiation_states():
                    # reshape state to a 1D array
                    state = np.reshape(state, (1, 64))
                    #get the index of 1 in state
                    index = np.where(state == 1)

                    # iterate over all the termination states
                    for term_state in option.list_termination_states():
                        # reshape state to a 1D array
                        term_state = np.reshape(term_state, (1, 64))
                        #get the index of 1 in state
                        term_index = np.where(term_state == 1)
                        # add the edge to the graph
                        graph[index, term_index] = mdp_cost
            
            print("mdp_name: ", mdp[0])
            
            cost_ind += 1

        return graph
    
    def build_graph_new(self):
        graph = Graph(64)

        cost_ind = 1
        # iterate over all the mdps
        for mdp in self.mdps:
            mdp_cost = cost_ind

            # iterate over all the options
            for option in mdp:

                # Q: how to represent a weighted graph? 
                # iterate over all the initiation states
                for state in option.list_initiation_states():
                    # reshape state to a 1D array
                    state_n = np.reshape(state, (64, ))
                    #get the index of 1 in state
                    index = np.where(state_n == 1)[0][0]
                    #print("index: ", index, state_n)

                    # iterate over all the termination states
                    for term_state in option.list_termination_states():
                        # reshape state to a 1D array
                        term_state_n = np.reshape(term_state, (64, ))
                        #get the index of 1 in state
                        term_index = np.where(term_state_n == 1)[0][0]
                        # add the edge to the graph
                        #graph[index, term_index] = mdp_cost
                        #print(index, term_index, mdp_cost)
                        graph.addEdge(index, term_index, mdp_cost)
            
            
            cost_ind += 1

        self.graph = graph
        return graph
    
    def find_shortest_path(self, start, end):
        self.graph.dijkstra(start, end)
    
class Heap():
 
    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []
 
    def newMinHeapNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode
 
    # A utility function to swap two nodes
    # of min heap. Needed for min heapify
    def swapMinHeapNode(self, a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t
 
    # A standard function to heapify at given idx
    # This function also updates position of nodes
    # when they are swapped.Position is needed
    # for decreaseKey()
    def minHeapify(self, idx):
        smallest = idx
        left = 2*idx + 1
        right = 2*idx + 2
 
        if (left < self.size and
           self.array[left][1]
            < self.array[smallest][1]):
            smallest = left
 
        if (right < self.size and
           self.array[right][1]
            < self.array[smallest][1]):
            smallest = right
 
        # The nodes to be swapped in min
        # heap if idx is not smallest
        if smallest != idx:
 
            # Swap positions
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest
 
            # Swap nodes
            self.swapMinHeapNode(smallest, idx)
 
            self.minHeapify(smallest)
 
    # Standard function to extract minimum
    # node from heap
    def extractMin(self):
 
        # Return NULL wif heap is empty
        if self.isEmpty() == True:
            return
 
        # Store the root node
        root = self.array[0]
 
        # Replace root node with last node
        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode
 
        # Update position of last node
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1
 
        # Reduce heap size and heapify root
        self.size -= 1
        self.minHeapify(0)
 
        return root
 
    def isEmpty(self):
        return True if self.size == 0 else False
 
    def decreaseKey(self, v, dist):
 
        # Get the index of v in  heap array
 
        i = self.pos[v]
 
        # Get the node and update its dist value
        self.array[i][1] = dist
 
        # Travel up while the complete tree is
        # not heapified. This is a O(Logn) loop
        while (i > 0 and self.array[i][1] <
                  self.array[(i - 1) // 2][1]):
 
            # Swap this node with its parent
            self.pos[ self.array[i][0] ] = (i-1)//2
            self.pos[ self.array[(i-1)//2][0] ] = i
            self.swapMinHeapNode(i, (i - 1)//2 )
 
            # move to parent index
            i = (i - 1) // 2;
 
    # A utility function to check if a given
    # vertex 'v' is in min heap or not
    def isInMinHeap(self, v):
 
        if self.pos[v] < self.size:
            return True
        return False
 
 

 
class Graph():
 
    def __init__(self, V):
        self.V = V
        self.graph = defaultdict(list)
 
    # Adds an edge to an undirected graph
    def addEdge(self, src, dest, weight):
 
        # Add an edge from src to dest.  A new node
        # is added to the adjacency list of src. The
        # node is added at the beginning. The first
        # element of the node has the destination
        # and the second elements has the weight
        newNode = [dest, weight]
        self.graph[src].insert(0, newNode)
 
        # Since graph is undirected, add an edge
        # from dest to src also
        newNode = [src, weight]
        self.graph[dest].insert(0, newNode)
 
    # The main function that calculates distances
    # of shortest paths from src to all vertices.
    # It is a O(ELogV) function
    def dijkstra(self, src, dest):
        parent = []
        path_list = []

        V = self.V  # Get the number of vertices in graph
        dist = []   # dist values used to pick minimum
                    # weight edge in cut
 
        # minHeap represents set E
        minHeap = Heap()
 
        #  Initialize min heap with all vertices.
        # dist value of all vertices
        for v in range(V):
            parent.append(-1)
            dist.append(1e7)
            minHeap.array.append( minHeap.newMinHeapNode(v, dist[v]))
            minHeap.pos.append(v)
 
        # Make dist value of src vertex as 0 so
        # that it is extracted first
        minHeap.pos[src] = src
        dist[src] = 0
        minHeap.decreaseKey(src, dist[src])
 
        # Initially size of min heap is equal to V
        minHeap.size = V
 
        # In the following loop,
        # min heap contains all nodes
        # whose shortest distance is not yet finalized.
        while minHeap.isEmpty() == False:
 
            # Extract the vertex
            # with minimum distance value
            newHeapNode = minHeap.extractMin()
            u = newHeapNode[0]
 
            # Traverse through all adjacent vertices of
            # u (the extracted vertex) and update their
            # distance values
            for pCrawl in self.graph[u]:
 
                v = pCrawl[0]
 
                # If shortest distance to v is not finalized
                # yet, and distance to v through u is less
                # than its previously calculated distance
                if (minHeap.isInMinHeap(v) and dist[u] != 1e7 and pCrawl[1] + dist[u] < dist[v]):
                        dist[v] = pCrawl[1] + dist[u]
                        parent[v] = u
                        if v == dest or u == dest:
                            path_list.append([u,v])
                        # update distance value
                        # in min heap also
                        minHeap.decreaseKey(v, dist[v])
 
        printArr(dist,V)
        #printArr_parent(parent, V)
        #print(path_list)


def printArr(dist, n):
    print ("Vertex\tDistance from source")
    for i in range(n):
        print ("%d\t\t%d" % (i,dist[i]))
    
def printArr_parent(parent, n):
    for i in range(1, n):
        print("% d - % d" % (parent[i], i))

if __name__ == "__main__":

    directions = ["left","right","up","down"]
    for i in range(8):
        for j in range (8):
            for direction in directions:
                mdp_0_placeholder.append(Action((i,j),direction))

    mdp_0 = mdp_0_placeholder

    mdp_1 = [
        Option("room_1_quad_1->room_1_quad_2"), Option("room_1_quad_1->room_1_quad_3"),
        Option("room_1_quad_2->room_1_quad_1"), Option("room_1_quad_2->room_1_quad_4"),
        Option("room_1_quad_3->room_1_quad_1"), Option("room_1_quad_3->room_1_quad_4"),
        Option("room_1_quad_4->room_1_quad_2"), Option("room_1_quad_4->room_1_quad_3"),

        Option("room_2_quad_1->room_2_quad_2"), Option("room_2_quad_1->room_2_quad_3"),
        Option("room_2_quad_2->room_2_quad_1"), Option("room_2_quad_2->room_2_quad_4"),
        Option("room_2_quad_3->room_2_quad_1"), Option("room_2_quad_3->room_2_quad_4"),
        Option("room_2_quad_4->room_2_quad_2"), Option("room_2_quad_4->room_2_quad_3"),

        Option("room_3_quad_1->room_3_quad_2"), Option("room_3_quad_1->room_3_quad_3"),
        Option("room_3_quad_2->room_3_quad_1"), Option("room_3_quad_2->room_3_quad_4"),
        Option("room_3_quad_3->room_3_quad_1"), Option("room_3_quad_3->room_3_quad_4"),
        Option("room_3_quad_4->room_3_quad_2"), Option("room_3_quad_4->room_3_quad_3"),

        Option("room_4_quad_1->room_4_quad_2"), Option("room_4_quad_1->room_4_quad_3"),
        Option("room_4_quad_2->room_4_quad_1"), Option("room_4_quad_2->room_4_quad_4"),
        Option("room_4_quad_3->room_4_quad_1"), Option("room_4_quad_3->room_4_quad_4"),
        Option("room_4_quad_4->room_4_quad_2"), Option("room_4_quad_4->room_4_quad_3"),
    ]


    mdp_2 = [
            Option("room_1->room_2"), Option("room_1->room_3"),
            Option("room_2->room_1"), Option("room_2->room_4"),
            Option("room_3->room_1"), Option("room_3->room_4"),
            Option("room_4->room_2"), Option("room_4->room_3"),
        ]
    # time execution of the graph planner
    
    #start_time = time.time()
    graph_planner = GraphPlanner([mdp_2, mdp_1])
    graph = graph_planner.build_graph_new()

    #print(graph)
    print(graph_planner.find_shortest_path(0, 54))
    #print("--- %s seconds ---" % (time.time() - start_time))
