# searchAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the project
description for details.

Good luck and happy searching!
"""

from game import Directions
from game import Agent
from game import Actions
from ghostAgents import GhostAgent
import util
import time
import search
import sys

class SearchGhostAgent(GhostAgent):
    """
    This ghost agent finds a path using a supplied search algorithm for a 
    supplied search problem, then returns a distribution over actions to follow that path.
    
    This follows the same pattern as Berkeley's SearchAgent but adapted for ghosts.
    """

    def __init__(self, index, fn='depthFirstSearch', prob='GhostPositionSearchProblem', heuristic='nullHeuristic'):
        GhostAgent.__init__(self, index)
        
        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        self.searchFunction = func

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print(f'[SearchGhostAgent] using problem type {prob}')

        if heuristic not in dir(search):
            raise AttributeError(heuristic + ' is not a heuristic function in search.py.')
        self.heuristicFunc = getattr(search, heuristic)

        # For metrics tracking
        self.searchTime = 0
        self.memoryUsage = 0
        self.expanded = 0
        self.visitedPositions = []
        self.goal = None

    def displayMetrics(self):
        """
        Display the performance metrics of the search.
        """
        print("\n" + "=" * 50)
        print(f"SEARCH COMPLETED - METRICS ({self.__class__.__name__}):")
        print(f"Search time: {self.searchTime:.5f} seconds")
        print(f"Memory usage: {self.memoryUsage} bytes")
        print(f"Expanded nodes: {self.expanded}")
        print(f"Total visited positions: {len(self.visitedPositions)}")
        print("=" * 50 + "\n")

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game board.
        Here, we choose a path to Pacman. All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: 
            raise Exception("No search function provided for SearchGhostAgent")
        
        starttime = time.time()
        
        # Create a new search problem
        problem = self.searchType(state, self.index)  # Pass ghost index to the problem
        
        # Find a path
        self.problem = problem
        self.goal = problem.goal
        self.actions = self.searchFunction(problem, self.heuristicFunc)

        # Get metrics
        totalCost = problem.getCostOfActions(self.actions)
        self.searchTime = time.time() - starttime
        self.expanded = problem._expanded if '_expanded' in dir(problem) else 0
        self.visitedPositions = problem._visitedlist if '_visitedlist' in dir(problem) else []
        self.memoryUsage = sys.getsizeof(problem._visited) + sys.getsizeof(problem._visitedlist) if '_visited' in dir(problem) else 0
        import __main__
        if hasattr(__main__, '_display'):
            __main__._display.drawExpandedCells(problem._visitedlist)
        
        # Display results
        self.displayMetrics()
        
        # Initialize action index
        self.actionIndex = 0

    def getDistribution(self, state):
        """
        Returns a distribution with 100% probability on the next action in the path.
        Returns a uniform distribution if there are no more actions.

        state: a GameState object (pacman.py)
        """
        # Initialize the search if this is the first call
        if 'actions' not in dir(self) or 'actionIndex' not in dir(self):
            self.registerInitialState(state)
            
        currentPacman = state.getPacmanPosition()
        if currentPacman != self.goal:
            # Pac‑man moved! replan from our current ghost pos
            ghostPos = state.getGhostPosition(self.index)
            problem = self.searchType(
                state,
                self.index,
                goal=currentPacman,
                start=ghostPos
            )
            self.goal = currentPacman
            self.actions = self.searchFunction(problem, self.heuristicFunc)
            self.visitedPositions = problem._visitedlist
            self.actionIndex = 0
        
        # Create distribution
        dist = util.Counter()

        # Get next action if available
        if self.actionIndex < len(self.actions):
            nextAction = self.actions[self.actionIndex]
            self.actionIndex += 1
            
            # Check if the action is legal
            if nextAction in state.getLegalActions(self.index):
                dist[nextAction] = 1.0
                return dist

        for a in state.getLegalActions(self.index):
            dist[a] += 1.0
        return dist


class GhostPositionSearchProblem(search.SearchProblem):
    """
    A search problem for a ghost to find Pacman.
    The state space consists of (x,y) positions in a pacman game.
    """

    def __init__(self, gameState, ghostIndex, costFn=lambda x: 1, goal=None, start=None, warn=True, visualize=True):
        """
        Stores the start and goal.
        """
        self.walls = gameState.getWalls()
        self.ghostIndex = ghostIndex
        self.startState = gameState.getGhostPosition(ghostIndex)
        if start != None: self.startState = start
        self.goal = gameState.getPacmanPosition()
        if goal != None: self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        
        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal
        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.
        """
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        # Bookkeeping for display purposes
        self._expanded += 1
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        """
        if actions == None: return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x, y))
        return cost

# Specific ghost implementations
class BFSGhost(SearchGhostAgent):
    """
    Ghost agent that uses BFS to find Pacman.
    """
    def __init__(self, index):
        SearchGhostAgent.__init__(self, index, fn='bfs')

class DFSGhost(SearchGhostAgent):
    """
    Ghost agent that uses DFS to find Pacman.
    """
    def __init__(self, index):
        SearchGhostAgent.__init__(self, index, fn='dfs')

class UCSGhost(SearchGhostAgent):
    """
    Ghost agent that uses UCS to find Pacman.
    """
    def __init__(self, index):
        SearchGhostAgent.__init__(self, index, fn='ucs')

class AStarGhost(SearchGhostAgent):
    """
    Ghost agent that uses A* with Manhattan heuristic to find Pacman.
    """
    def __init__(self, index):
        SearchGhostAgent.__init__(self, index, fn='astar', heuristic='manhattanHeuristic')