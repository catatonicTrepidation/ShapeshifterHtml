# search.py
# Original Pacman Search Project found @
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

# Astar is the only algorithm used in shapeshifter
# None of the other general search algorithms are used
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    startstate = problem.getStartState()
    sol = []
    frontier = util.Stack()
    frontier.push(startstate)
    explored = set()
    actions = {}
    actions[startstate] = []
    while not frontier.isEmpty():
        parentstate = frontier.pop()
        if parentstate not in explored:
            if problem.isGoalState(parentstate):
                return actions[parentstate]
            explored.add(parentstate)
            successors = problem.getSuccessors(parentstate)
            for childstate, action, cost in successors:
                frontier.push(childstate)
                actions[childstate] = actions[parentstate] + [action]
    return []

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    startstate = problem.getStartState()
    #print('search.py: startstate =',startstate)
    sol = []
    frontier = util.Queue()
    frontier.push((startstate,[]))
    explored = set()
    while not frontier.isEmpty():
        parentstate, prevactions = frontier.pop()
        if parentstate not in explored:
            if problem.isGoalState(parentstate):
                return prevactions
            explored.add(parentstate)
            for childstate, action, cost in problem.getSuccessors(parentstate):
                #print 'childstate =',childstate,' | action =',action,'| cost =',cost
                frontier.push((childstate, prevactions + [action]))
    return []

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    startstate = problem.getStartState()
    sol = []
    frontier = util.PriorityQueue()
    frontier.push((startstate,[]), 0)
    explored = set()
    while not frontier.isEmpty():
        parentstate, prevactions = frontier.pop()
        if parentstate not in explored:
            if problem.isGoalState(parentstate):
                return prevactions
            explored.add(parentstate)
            for childstate, action, cost in problem.getSuccessors(parentstate):
                frontier.push((childstate, prevactions + [action]), problem.getCostOfActions(prevactions + [action]))
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."

    solution = []
    listToFetch = util.PriorityQueue()
    listToFetch.push((problem.getStartState(), solution), 0)
    # print "Cost: ", problem.getCostOfActions(solution);

    # visited states backed by set
    visitedStates = set()

    while not listToFetch.isEmpty():
        state, path = listToFetch.pop()

        # register in visited spots
        if state not in visitedStates:
            visitedStates.add(state)

            solution = path
            # explore if not in visited states
            # print "visited", visitedStates


            # i[] = (coordinate, direction, stepCost)

            if (problem.isGoalState(state)):
                # print "final sol1: ", solution;
                return solution

            newSet = problem.getSuccessors(state)
            for currentstate, step, cost in newSet:
                if currentstate not in visitedStates:

                    listToFetch.push((currentstate, solution + [step]),
                                     problem.getCostOfActions(solution) + cost + heuristic(currentstate, problem=problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
