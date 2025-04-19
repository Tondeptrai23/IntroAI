# search.py
# ---------
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

from searchAgents import SearchGhostAgent
from game import Directions
import util
from util import manhattanDistance

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class PacmanSearchProblem(SearchProblem):
    """
    A search problem for finding a path to Pacman from a ghost's position.
    """

    def __init__(self, gameState, ghostIndex, visitedList=None, expanded=None):
        """
        Stores the information necessary to solve the problem.
        gameState: A GameState object (pacman.py)
        ghostIndex: The index of the ghost agent
        visitedList: A list to track the visited positions
        expanded: A counter for expanded nodes
        """
        self.gameState = gameState
        self.ghostIndex = ghostIndex
        self.startState = gameState.getGhostPosition(ghostIndex)
        self.goalState = gameState.getPacmanPosition()
        self.walls = gameState.getWalls()
        self.visitedList = visitedList if visitedList is not None else []
        self.expanded = expanded if expanded is not None else 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        return state == self.goalState

    def getSuccessors(self, state):
        """
        Returns the successors of the current state.
        """
        self.expanded += 1
        
        successors = []
        x, y = state
        
        # Track visited positions (for visualization)
        if state not in self.visitedList:
            self.visitedList.append(state)
        
        # Get legal actions from the current state
        # Consider all four directions
        for action, (dx, dy) in [
            (Directions.NORTH, (0, 1)),
            (Directions.SOUTH, (0, -1)),
            (Directions.EAST, (1, 0)),
            (Directions.WEST, (-1, 0))
        ]:
            next_x, next_y = int(x + dx), int(y + dy)
            
            # Check if the next position is valid (not a wall)
            if not self.walls[next_x][next_y]:
                nextState = (next_x, next_y)
                cost = 1.0  # Uniform cost for now
                successors.append((nextState, action, cost))
        
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        """
        if actions is None:
            return float('inf')
            
        cost = 0
        for action in actions:
            cost += 1  # Uniform cost for now
            
        return cost

# Search algorithm implementations
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    # TODO: Implement BFS here
    # Remember to update problem.visitedList for visualization
    
    # Return a list of actions that leads from the start state to the goal state
    return []

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    # TODO: Implement DFS here
    # Remember to update problem.visitedList for visualization
    
    # Return a list of actions that leads from the start state to the goal state
    return []

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    # TODO: Implement UCS here
    # Remember to update problem.visitedList for visualization
    
    # Return a list of actions that leads from the start state to the goal state
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem. This heuristic is trivial.
    """
    return 0

def manhattanHeuristic(state, problem=None):
    """
    The Manhattan distance heuristic for a Pacman search problem.
    """
    xy1 = state
    xy2 = problem.goalState
    return manhattanDistance(xy1, xy2)

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # TODO: Implement A* search here
    # Remember to update problem.visitedList for visualization
    
    # Return a list of actions that leads from the start state to the goal state
    return []



# Actual Ghost implementations using the search algorithms
class BFSGhost(SearchGhostAgent):
    """Ghost that uses Breadth-First Search (BFS) to choose actions."""
    
    def __init__(self, index):
        super().__init__(index)
        self.color = "blue"  # Set ghost color to blue
    
    def findPathToPacman(self, state):
        """
        Use BFS to compute a path to Pacman.
        """
        # Create a search problem
        problem = PacmanSearchProblem(state, self.index, self._visitedlist, self._expanded)
        
        # Use BFS to find a path
        path = breadthFirstSearch(problem)
        
        # Update expanded nodes count
        self._expanded = problem.expanded
        
        return path

class DFSGhost(SearchGhostAgent):
    """Ghost that uses Depth-First Search (DFS) to choose actions."""
    
    def __init__(self, index):
        super().__init__(index)
        self.color = "pink"  # Set ghost color to pink
    
    def findPathToPacman(self, state):
        """
        Use DFS to compute a path to Pacman.
        """
        # Create a search problem
        problem = PacmanSearchProblem(state, self.index, self._visitedlist, self._expanded)
        
        # Use DFS to find a path
        path = depthFirstSearch(problem)
        
        # Update expanded nodes count
        self._expanded = problem.expanded
        
        return path

class UCSGhost(SearchGhostAgent):
    """Ghost that uses Uniform-Cost Search (UCS) to choose actions."""
    
    def __init__(self, index):
        super().__init__(index)
        self.color = "orange"  # Set ghost color to orange
    
    def findPathToPacman(self, state):
        """
        Use UCS to compute a path to Pacman.
        """
        # Create a search problem
        problem = PacmanSearchProblem(state, self.index, self._visitedlist, self._expanded)
        
        # Use UCS to find a path
        path = uniformCostSearch(problem)
        
        # Update expanded nodes count
        self._expanded = problem.expanded
        
        return path

class AStarGhost(SearchGhostAgent):
    """Ghost that uses A* Search to choose actions."""
    
    def __init__(self, index):
        super().__init__(index)
        self.color = "red"  # Set ghost color to red
    
    def findPathToPacman(self, state):
        """
        Use A* Search to compute a path to Pacman.
        """
        # Create a search problem
        problem = PacmanSearchProblem(state, self.index, self._visitedlist, self._expanded)
        
        # Use A* to find a path with the Manhattan distance heuristic
        path = aStarSearch(problem, manhattanHeuristic)
        
        # Update expanded nodes count
        self._expanded = problem.expanded
        
        return path