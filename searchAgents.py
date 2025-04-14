# Modified ghostAgents.py
import time
import tracemalloc
from game import Agent
from game import Actions
from game import Directions
import random
from ghostAgents import GhostAgent
from util import manhattanDistance
import util
import time
import sys

class SearchGhostAgent(GhostAgent):
    """A base class for ghosts that use search algorithms."""
    
    def __init__(self, index):
        GhostAgent.__init__(self, index)
        self._visited = {}  # Dictionary to track visited positions
        self._visitedlist = []  # List of visited positions for display
        self._expanded = 0  # Counter for expanded nodes
        self.start_time = time.time()  # Start time for tracking search time
        self.metrics_printed = False  # Flag to ensure metrics are only printed once
    
    def getAction(self, state):
        """Get the action to take based on the state."""
        # Get the current position
        pos = state.getGhostPosition(self.index)
        
        # Track visited positions
        if pos not in self._visited:
            self._visited[pos] = True
            self._visitedlist.append(pos)
        
        # Increment expanded nodes counter
        self._expanded += 1
        
        # Check if Pacman is close by
        pacmanPos = state.getPacmanPosition()
        if manhattanDistance(pos, pacmanPos) <= 1.5 and not self.metrics_printed:
            self.printMetrics()
        
        # Check if game is about to end
        if (state.isLose() or state.isWin()) and not self.metrics_printed:
            self.printMetrics()
        
        # Visualize expanded cells
        self.drawExpandedCells()
        
        # Get action distribution and choose action
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)
        
    def printMetrics(self):
        """Calculate and print search metrics."""
        if self.metrics_printed:
            return
            
        self.metrics_printed = True
        
        # Search time
        elapsed_time = time.time() - self.start_time
        
        # Memory usage estimate
        memory_usage = sys.getsizeof(self._visited) + sys.getsizeof(self._visitedlist)
        for pos in self._visitedlist:
            memory_usage += sys.getsizeof(pos)
        
        # Print metrics
        print("\n" + "=" * 50)
        print("SEARCH COMPLETED - METRICS:")
        print(f"Search time: {elapsed_time:.5f} seconds")
        print(f"Memory usage estimate: {memory_usage} bytes")
        print(f"Expanded nodes: {self._expanded}")
        print(f"Total visited positions: {len(self._visitedlist)}")
        print("=" * 50 + "\n")
    
    def drawExpandedCells(self):
        """Draw expanded cells on the UI."""
        import __main__
        if '_display' in dir(__main__):
            if 'drawExpandedCells' in dir(__main__._display):
                __main__._display.drawExpandedCells(self._visitedlist)
                
    def final(self, state):
        """Called at the end of the game."""
        # Ensure metrics are printed at the end of the game if not already
        if not self.metrics_printed:
            self.printMetrics()


class LeftMoveOnlyGhost(SearchGhostAgent):
    """A ghost that always tries to move left (West) when possible and tracks metrics."""
    
    def __init__(self, index):
        super().__init__(index)
    
    def getDistribution(self, state):
        """Get the distribution over actions."""
        dist = util.Counter()
        legalActions = state.getLegalActions(self.index)
        
        # Remove STOP action if present
        if Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)
        
        # Prefer WEST (left) if possible
        if Directions.WEST in legalActions:
            dist[Directions.WEST] = 1.0
        else:
            # If we can't move left, pick randomly among other legal actions
            for action in legalActions:
                dist[action] = 1.0
            dist.normalize()
        
        return dist

class RightMoveOnlyGhost(SearchGhostAgent):
    """A ghost that always tries to move right (East) when possible and tracks metrics."""
    
    def __init__(self, index):
        super().__init__(index)
    
    def getDistribution(self, state):
        """Get the distribution over actions."""
        dist = util.Counter()
        legalActions = state.getLegalActions(self.index)
        
        # Remove STOP action if present
        if Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)
        
        # Prefer EAST (right) if possible
        if Directions.EAST in legalActions:
            dist[Directions.EAST] = 1.0
        else:
            # If we can't move right, pick randomly among other legal actions
            for action in legalActions:
                dist[action] = 1.0
            dist.normalize()
        
        return dist