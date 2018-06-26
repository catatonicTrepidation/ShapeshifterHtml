# Original Code: Pacman search code from
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
import search
import re
from ast import literal_eval

class ShapeShifterSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  ShapeShifter Puzzle domain
      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self,startState,numranks,cycle):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.startState = startState
        self.numranks = numranks
        self._expanded = 0
        self.cycle = cycle
        self.goal_rank = cycle[2]

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        #print 'isGoalState: state =',state
        # if (len(state[1])**2)%(len(state[1])**2 + sum([sum(row) for row in state[1]])) == 0:
        #     print('state =', state)
        for row in state[1]:
            for c in row:
                if c != self.goal_rank:
                    return False

        return len(state[0]) == 0

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        numranks = self.numranks
        piecesleft, gamemap = state
        # print('state =',state)
        # print()
        # print('piecesleft =',piecesleft)
        if len(piecesleft) == 0: return []
        #print('piecesleft[0] =',piecesleft[0])
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
                for n in range(pieceheight):
                    for m in range(piecewidth):
                        newmap[n + j][m + i] = (newmap[n + j][m + i] + piece[n][m]) % numranks
                newmap = tuple([tuple(row) for row in newmap])
                successors.append(((tuple(piecesleft[1:]), newmap), (i,j), 0))

        self._expanded += 1
        #print 'successors =',successors
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        This is how the heuristic costs are implemented.
        If those actions include an illegal move, return a hefty number.
        """
        return len(actions)

def shapeshifterHeuristic(state, problem):
    """
    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use.
    """
    # change to sum of differences between goal_rank and cur_rank of each square?
    piecesleft, gamemap = state
    #if sum(sum([(y - problem.goal_rank) for y in x]) for x in gamemap) < 2:
    #    print('gamemap =',gamemap)

    topleftcorner = gamemap[0][0]
    toprightcorner = gamemap[0][len(gamemap)-1]
    bottomleftcorner = gamemap[len(gamemap)-1][0]
    bottomrightcorner = gamemap[len(gamemap)-1][len(gamemap)-1]

    rotationsum = topleftcorner+toprightcorner+bottomrightcorner+bottomleftcorner
#    magic = (rotationsum) % (3) - len(piecesleft)
    magic = (rotationsum) - len(piecesleft)


    #return (magic);

    htotal = 0


    #3 = 44198
    #6 = 39248
    #7 = 13691
    #8 = 39444
    #9 = 47419
    if (len(piecesleft) > 7): #you can only rotate the four corners up to 2 times, so anything greater defeats this precision
        for x in gamemap:
            for y in x:
                #htotal = htotal + bool(y != problem.goal_rank)
                htotal = (htotal + y) #the more rotations the further away
    else:
        for x in gamemap:
            for y in x:
                htotal = htotal + bool(y != problem.goal_rank) #the more rotations, the less of a difference
                #htotal = (htotal + y)

    # htotal = htotal + bool(topleftcorner != problem.goal_rank) + len(piecesleft)
    # htotal = htotal + bool(toprightcorner != problem.goal_rank) + len(piecesleft)
    # htotal = htotal + bool(bottomleftcorner != problem.goal_rank) + len(piecesleft)
    # htotal = htotal + bool(bottomrightcorner != problem.goal_rank) + len(piecesleft)


    #print out every time there is a super close solutions
    if (htotal) < 4:
        print('gamemap =',gamemap)

    return htotal
    #return sum(sum([(y - problem.goal_rank) for y in x]) for x in gamemap)
    #return sum(sum([bool(y != problem.goal_rank) for y in x]) for x in gamemap)


#SHAPESHIFTER_DATA = ((2,1,0,0),(2,1,0,0),(0,0,2,0),(2,1,2,2)) OLD
#SHAPESHIFTER_DATA = ((2,0,2,0), (2,1,2,1), (1,1,2,1), (2,2,0,2)) OLD
#SHAPESHIFTER_DATA = ((1,2,2,0), (2,1,2,0), (2,0,0,1), (1,1,0,2)) OLD
#SHAPESHIFTER_DATA = ((2,0,0,2), (1,1,1,0), (1,1,0,2), (0,1,2,1))
#SHAPESHIFTER_DATA = ((0,1,2,2),(0,1,2,2),(2,2,0,2),(2,1,2,2))
#SHAPESHIFTER_DATA = ((0,0,2,2),(0,0,2,2),(0,2,0,1),(0,0,1,1))
#SHAPESHIFTER_DATA = ((0,1,2,2),(2,1,2,2),(1,0,0,1),(0,0,1,2)) #first 4
#SHAPESHIFTER_DATA = ((2,2,2,2),(1,2,1,2),(0,2,2,1),(0,0,0,1))
if __name__ == "__main__":
    """
    # pieces = (
    #           ((3,3), ((0,1,1,0),(0,1,1,0),(1,1,0,0),(0,0,0,0))),
    #           ((2,2), ((1,1,0,0),(1,1,0,0),(0,0,0,0),(0,0,0,0))),
    #           ((3,3), ((1,0,1,0),(1,0,1,0),(1,1,1,0),(0,0,0,0))),
    #           ((3,3), ((1,0,0,0),(1,1,1,0),(0,0,1,0),(0,0,0,0))),
    #           ((2,2), ((1,0,0,0),(1,1,0,0),(0,0,0,0),(0,0,0,0))),
    #           ((2,3), ((1,1,0,0),(0,1,0,0),(1,1,0,0),(0,0,0,0))),
    #           ((3,3), ((1, 1, 0, 0), (0, 1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 0))),
    #           ((3, 2), ((0, 1, 0, 0), (1, 1, 1, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
    #           ((3, 3), ((1, 0, 1, 0), (1, 1, 1, 0), (1, 0, 1, 0), (0, 0, 0, 0))),
    #           ((2, 1), ((1, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
    #           ((3, 3), ((0, 1, 0, 0), (1, 1, 1, 0), (0, 1, 0, 0), (0, 0, 0, 0)))
    # )
    pieces = (
        ((3, 3), ((1, 1, 1, 0), (1, 0, 0, 0), (1, 0, 0, 0), (0, 0, 0, 0))),  #upsdwn L
        ((3, 3), ((1, 0, 0, 0), (1, 1, 1, 0), (0, 0, 1, 0), (0, 0, 0, 0))),  #grub screw
        ((2, 2), ((1, 1, 0, 0), (1, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),  #square
        ((3, 3), ((1, 1, 0, 0), (0, 1, 1, 0), (0, 0, 1, 0), (0, 0, 0, 0))),  #french fry
        ((3, 3), ((1, 1, 0, 0), (1, 1, 0, 0), (0, 1, 1, 0), (0, 0, 0, 0))),  #q
        ((3, 3), ((1, 1, 1, 0), (0, 1, 0, 0), (1, 1, 1, 0), (0, 0, 0, 0))),  #エ
        ((2, 3), ((1, 1, 0, 0), (0, 1, 0, 0), (1, 1, 0, 0), (0, 0, 0, 0))),  #bckwrd c
        ((3, 3), ((1, 1, 1, 0), (1, 0, 0, 0), (1, 0, 0, 0), (0, 0, 0, 0))),  #upsdwn L
        ((3, 2), ((1, 1, 0, 0), (0, 1, 1, 0), (0, 0, 0, 0), (0, 0, 0, 0))),  # -\_
        ((2, 3), ((1, 1, 0, 0), (1, 1, 0, 0), (1, 1, 0, 0), (0, 0, 0, 0))),  #ビル
        ((3, 3), ((1, 0, 0, 0), (1, 1, 1, 0), (1, 0, 0, 0), (0, 0, 0, 0))),  #|--
    )
    pieces = (
        ((3, 3), ((1, 1, 1, 0), (1, 0, 1, 0), (1, 1, 1, 0), (0, 0, 0, 0))),  # ring
        ((3, 2), ((1, 1, 1, 0), (0, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),  # short T
        ((2, 3), ((0, 1, 0, 0), (1, 1, 0, 0), (0, 1, 0, 0), (0, 0, 0, 0))),  # -|
        ((2, 3), ((1, 0, 0, 0), (1, 1, 0, 0), (1, 0, 0, 0), (0, 0, 0, 0))),  # |-
        ((2, 2), ((0, 1, 0, 0), (1, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),  # _|
        ((2, 2), ((1, 1, 0, 0), (0, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),  # ‾|
        ((3, 3), ((0, 1, 1, 0), (0, 1, 0, 0), (1, 1, 1, 0), (0, 0, 0, 0))),  # bckwrd ユ
        ((3, 3), ((0, 0, 1, 0), (0, 1, 1, 0), (1, 1, 1, 0), (0, 0, 0, 0))),  # 右階段
        ((3, 3), ((1, 0, 0, 0), (1, 1, 1, 0), (0, 0, 1, 0), (0, 0, 0, 0))),  # grub screw
        ((2, 3), ((1, 0, 0, 0), (1, 1, 0, 0), (0, 1, 0, 0), (0, 0, 0, 0))),  # 左蛞蝓
        ((3, 3), ((0, 1, 0, 0), (1, 1, 1, 0), (0, 1, 0, 0), (0, 0, 0, 0))),  # +
    )
    pieces = (
        ((2, 2), ((1, 1, 0, 0), (0, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),  # ‾|
        ((3, 3), ((0, 0, 1, 0), (1, 1, 1, 0), (1, 0, 0, 0), (0, 0, 0, 0))),  # bckwrd grub screw
        ((3, 3), ((1, 1, 1, 0), (1, 0, 1, 0), (1, 1, 1, 0), (0, 0, 0, 0))),  # ring
        ((2, 1), ((1, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),  # -
        ((3, 2), ((1, 1, 0, 0), (0, 1, 1, 0), (0, 0, 0, 0), (0, 0, 0, 0))),  # zig2
        ((2, 3), ((1, 1, 0, 0), (1, 1, 0, 0), (1, 1, 0, 0), (0, 0, 0, 0))),  # ビル
        ((1, 2), ((1, 0, 0, 0), (1, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),  # l
        ((3, 3), ((1, 1, 1, 0), (0, 1, 0, 0), (1, 1, 1, 0), (0, 0, 0, 0))),  # エ
        ((3, 3), ((1, 1, 0, 0), (1, 1, 0, 0), (0, 1, 1, 0), (0, 0, 0, 0))),  # q
        ((2, 3), ((1, 1, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), (0, 0, 0, 0))),  # 1‾
        ((3, 3), ((0, 1, 0, 0), (1, 1, 1, 0), (0, 1, 0, 0), (0, 0, 0, 0))),  # +
        ((3, 2), ((0, 1, 1, 0), (1, 1, 1, 0), (0, 0, 0, 0), (0, 0, 0, 0))),  # van
    )"""

    # pieces = (
    #     ((3, 3), ((1, 0, 1, 0), (1, 1, 1, 0), (0, 1, 0, 0), (0, 0, 0, 0))),  # Y
    # )


    import shapeshifter_html
    gamemap, pieces, cycle = shapeshifter_html.get_shapeshifter_config()

    pieces = (
              ((3,3), ((0,1,1,0),(0,1,1,0),(1,1,0,0),(0,0,0,0))),
              ((2,2), ((1,1,0,0),(1,1,0,0),(0,0,0,0),(0,0,0,0))),
              ((3,3), ((1,0,1,0),(1,0,1,0),(1,1,1,0),(0,0,0,0))),
              ((3,3), ((1,0,0,0),(1,1,1,0),(0,0,1,0),(0,0,0,0))),
              ((2,2), ((1,0,0,0),(1,1,0,0),(0,0,0,0),(0,0,0,0))),
              ((2,3), ((1,1,0,0),(0,1,0,0),(1,1,0,0),(0,0,0,0))),
              ((3,3), ((1, 1, 0, 0), (0, 1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 0))),
              ((3, 2), ((0, 1, 0, 0), (1, 1, 1, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
              ((3, 3), ((1, 0, 1, 0), (1, 1, 1, 0), (1, 0, 1, 0), (0, 0, 0, 0))),
              ((2, 1), ((1, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
              ((3, 3), ((0, 1, 0, 0), (1, 1, 1, 0), (0, 1, 0, 0), (0, 0, 0, 0)))
    )

    #***Attempted Imported Array Level ***#
    with open('arraylevels/default1.txt', encoding="utf8") as f:
        read_data = f.readlines()
    for lines in read_data:
        read_data = lines.strip()
    # pieces = literal_eval("read_data")
    #-------------------------------------#

    gamemap = ((2, 1, 0, 0),(1, 0, 1, 0),(2, 2, 0, 0),(0, 0, 0, 0))
    path = [(0, 1), (0, 1), (0, 0), (0, 0), (0, 0), (0, 1), (0, 1), (0, 1), (0, 0), (1, 0), (0, 0)]
    startState = (pieces, gamemap)
    print('__main__: startState =',startState)
    problem = ShapeShifterSearchProblem(startState, numranks=3, cycle=[2,1,0])

    path = search.aStarSearch(problem, heuristic=shapeshifterHeuristic)
    print('path =',path)
    print(problem._expanded, "nodes expanded")
