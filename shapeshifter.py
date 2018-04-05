# coding=utf-8


# searchAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
This file contains all of the agents that can be selected to
control Pacman.  To select an agent, use the '-p' option
when running pacman.py.  Arguments can be passed to your agent
using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the
project description.

Please only change the parts of the file you are asked to.
Look for the lines that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the
project description for details.

Good luck and happy searching!
"""

import search




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
        print('len(state[0]) == 0 is', len(state[0]) == 0)
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
                successors.append(((tuple(piecesleft[1:]), newmap), (i,j), 1))

        self._expanded += 1
        #print 'successors =',successors
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999
        """
        return len(actions)

def shapeshifterHeuristic(state, problem):
    """
    Your heuristic for the ShapeShifterSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a
    Grid (see game.py) of either True or False. You can call foodGrid.asList()
    to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, problem.walls gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use. For example,
    if you only want to count the walls once and store that value, try:
      problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount']
    """
    # change to sum of differences between goal_rank and cur_rank of each square?
    piecesleft, gamemap = state
    if sum(sum([(y - problem.goal_rank) for y in x]) for x in gamemap) < 2:
        print('gamemap =',gamemap)

    return sum(sum([(y - problem.goal_rank) for y in x]) for x in gamemap)
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

    # pieces = (
    #     ((3, 3), ((0, 1, 1, 0), (0, 1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 0))),
    #     ((2, 2), ((1, 1, 0, 0), (1, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
    #     ((3, 3), ((1, 0, 1, 0), (1, 0, 1, 0), (1, 1, 1, 0), (0, 0, 0, 0))),
    #     ((3, 3), ((1, 0, 0, 0), (1, 1, 1, 0), (0, 0, 1, 0), (0, 0, 0, 0))),
    #     ((2, 2), ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
    #     ((2, 3), ((1, 1, 0, 0), (0, 1, 0, 0), (1, 1, 0, 0), (0, 0, 0, 0))),
    #     ((3, 2), ((0, 1, 0, 0), (1, 1, 1, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
    # )
    import shapeshifter_html
    gamemap, pieces, cycle = shapeshifter_html.get_shapeshifter_config()

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
    # gamemap = ((2, 1, 0, 0),(1, 0, 1, 0),(2, 2, 0, 0),(0, 0, 0, 0))
    # path = [(0, 1), (0, 1), (0, 0), (0, 0), (0, 0), (0, 1), (0, 1), (0, 1), (0, 0), (1, 0), (0, 0)]
    startState = (pieces, gamemap)
    print('__main__: startState =',startState)
    problem = ShapeShifterSearchProblem(startState, numranks=3, cycle=[1,2,0]) # speed does NOT seem to be a py3 vs py2 problem
    path = search.aStarSearch(problem, heuristic=shapeshifterHeuristic)
    print('path =',path)
    print(problem._expanded, "nodes expanded")

