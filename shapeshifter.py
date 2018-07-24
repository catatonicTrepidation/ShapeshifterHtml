# Original Code: Pacman search code from
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
import search


class ShapeShifterSearchProblem(search.SearchProblem):
    def __init__(self, start_state, cycle, goal):
        self.startState = start_state
        self.numranks = len(cycle)
        self._expanded = 0
        self.cycle = cycle
        self.goal_rank = goal

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        if len(state[0]) != 0:
            return False
        # no more pieces
        for row in state[1]:
            for c in row:
                if c != self.goal_rank:
                    return False

        return True

    def getSuccessors(self, state):
        """
        Return a list of triples: (successor, action, stepCost),
        'successor' are following states,
        'action' is the action required to get there
        'stepCost' is the incremental cost of expanding to that successor
        """
        numranks = self.numranks
        piecesleft, gamemap = state

        if len(piecesleft) == 0:
            return []

        piecesleft = list(piecesleft)
        successors = []
        dimensions, piece = piecesleft[0]
        piecewidth, pieceheight = dimensions
        piece = [list(row) for row in piece]
        mapwidth = len(gamemap[0])
        mapheight = len(gamemap)

        for j in range(mapheight - pieceheight + 1):
            for i in range(mapwidth - piecewidth + 1):
                newmap = [list(row) for row in gamemap]

                # "increment" and rotate the image
                for n in range(pieceheight):
                    for m in range(piecewidth):
                        newmap[n + j][m + i] = (newmap[n + j][m + i] + piece[n][m]) % numranks
                newmap = tuple([tuple(row) for row in newmap])
                successors.append(((tuple(piecesleft[1:]), newmap), (i, j), 0))

        self._expanded += 1

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        This is how the heuristic costs are implemented.
        """
        return len(actions)


# lower costs the closer it is to the solution
def heuristic1(state, problem):
    # return sum(sum([(y - problem.goal_rank) for y in x]) for x in gamemap)
    return sum(sum([bool(y != problem.goal_rank) for y in x]) for x in gamemap)

# see how close it is to the mod of the total number of state
# TODO: 7 is hard coded due to 4 corners and 3 states. Should fix this in future
def heuristic2(state, problem):
    """
        Node Counters
        3 = 44198
        6 = 39248
        7 = 13691
        8 = 39444
        9 = 47419
    """

    # change to sum of differences between goal_rank and cur_rank of each square?
    piecesleft, gamemap = state

    htotal = 0

    #TODO: Dynamic Programming to stash htotal

    if (len(piecesleft) > 7):
    #you can only rotate the four corners up to 2 times, so anything greater defeats this precision
        for x in gamemap:
            for y in x:
                #htotal = htotal + bool(y != problem.goal_rank)
                htotal = (htotal + y) #the more rotations the further away
    else:
        for x in gamemap:
            for y in x:
                htotal = htotal + bool(y != problem.goal_rank)
                #the more rotations, the less of a difference

    # htotal = (htotal + y)
    # htotal = htotal + bool(topleftcorner != problem.goal_rank) + len(piecesleft)
    # htotal = htotal + bool(toprightcorner != problem.goal_rank) + len(piecesleft)
    # htotal = htotal + bool(bottomleftcorner != problem.goal_rank) + len(piecesleft)
    # htotal = htotal + bool(bottomrightcorner != problem.goal_rank) + len(piecesleft)

    #print out every time there is a super close solutions
    if (htotal) < 2:
        print('Close Gamemap: ')
        for row in gamemap:
            print(row)
        print()
    return htotal

# attempted corner heuristic (doesn't work)
def heuristic3(state, problem):
    piecesleft, gamemap = state

    topleftcorner = gamemap[0][0]
    toprightcorner = gamemap[0][len(gamemap) - 1]
    bottomleftcorner = gamemap[len(gamemap) - 1][0]
    bottomrightcorner = gamemap[len(gamemap) - 1][len(gamemap) - 1]

    rotationsum = topleftcorner + toprightcorner + bottomrightcorner + bottomleftcorner
    #    magic = (rotationsum) % (3) - len(piecesleft)
    magic = (rotationsum) - len(piecesleft)
    return magic


if __name__ == "__main__":
    import shapeshifter_html

    # INSERT HTML LEVEL HERE
    # this prints the game state
    # shapeshifter_html.print_shapeshifter_html('htmllevels/level5.html')
    # this gets the pieces
    gamemap, pieces, cycle, goalpiece = shapeshifter_html.get_shapeshifter_config('htmllevels/level5.html')

    # uncomment for hardcoded level
    '''
    pieces = (
        ((3, 3), ((0, 1, 1, 0), (0, 1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 0))),
        ((2, 2), ((1, 1, 0, 0), (1, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
        ((3, 3), ((1, 0, 1, 0), (1, 0, 1, 0), (1, 1, 1, 0), (0, 0, 0, 0))),
        ((3, 3), ((1, 0, 0, 0), (1, 1, 1, 0), (0, 0, 1, 0), (0, 0, 0, 0))),
        ((2, 2), ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
        ((2, 3), ((1, 1, 0, 0), (0, 1, 0, 0), (1, 1, 0, 0), (0, 0, 0, 0))),
        ((3, 3), ((1, 1, 0, 0), (0, 1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 0))),
        ((3, 2), ((0, 1, 0, 0), (1, 1, 1, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
        ((3, 3), ((1, 0, 1, 0), (1, 1, 1, 0), (1, 0, 1, 0), (0, 0, 0, 0))),
        ((2, 1), ((1, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
        ((3, 3), ((0, 1, 0, 0), (1, 1, 1, 0), (0, 1, 0, 0), (0, 0, 0, 0)))
    )
    gamemap = ((2, 1, 0, 0),(1, 0, 1, 0),(2, 2, 0, 0),(0, 0, 0, 0))
    cycle = [0,1,2]
    goalpiece = 0
    '''

    startState = (pieces, gamemap)

    problem = ShapeShifterSearchProblem(startState, cycle=cycle, goal=goalpiece)
    path = search.aStarSearch(problem, heuristic=heuristic2)
    print('Path =', path)
    print(problem._expanded, "nodes expanded")