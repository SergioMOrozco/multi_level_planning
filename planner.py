from main import a_subset_b
def path(state, parents):
    route = [state]
    while parents[state] != None:
        state = parents[state]
        route = [state] + route
    return route

# termination conditions are an OR, which makes neighbourhoods an intersection rather than subset
def get_sucessors(S, options, N): #format: [sucessor, option]
    sucessors = set()
    for option in options:
        for state in option.list_initiation_states():
            if a_subset_b(S, N(S)):
                set.add([option.execute_policy(state), option])
    return sucessors
        

        

def bfs_planner(S, G, options, N):
    """
    Implement breadth-first search.
    Input:
        problem - the problem on which the search is conducted, a SearchProblem
    Output: a list of states representing the path of the solution
    """

    if a_subset_b(S, N(G)):
        # create and return the list of options
        print("HELP")
    reached = [S]
    frontier = queue.Queue() 
    parents = {S:None}
    frontier.put(S)
    while (not frontier.empty()):
        state = frontier.get()
        for i in get_sucessors(state, options, N):
            if problem.is_goal_state(i):
                parents[i] = state
                return path(i, parents)
            elif i not in reached:
                reached.append(i)
                parents[i] = state
                frontier.put(i)
    return []
