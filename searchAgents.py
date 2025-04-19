# Modified searchAgents.py
import time
from game import Agent
from game import Actions
from game import Directions
import random
from ghostAgents import GhostAgent
from util import manhattanDistance
import util
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
        
        # New variables for path planning
        self.path_computed = False
        self.path = []  # Will store the computed path
        self.current_path_index = 0
    
    def registerInitialState(self, state):
        """Called at the beginning of a game. Compute the path here."""
        # Optional: Initialize anything specific for the algorithm
        pass
    
    def findPathToPacman(self, state):
        """
        Compute a path to Pacman using the specific search algorithm.
        This should be implemented by subclasses.
        """
        util.raiseNotDefined()
    
    def getAction(self, state):
        """Get the action to take based on the state."""
        # Get the current position and pacman position
        ghostPos = state.getGhostPosition(self.index)
        pacmanPos = state.getPacmanPosition()
        
        # If we haven't computed a path yet, or Pacman has moved significantly, recompute
        if not self.path_computed or (self.path and self.current_path_index >= len(self.path)):
            # Start timing and reset tracking
            if not self.metrics_printed:
                self.start_time = time.time()
                self._visited = {}
                self._visitedlist = []
                self._expanded = 0
            
            # Compute the path
            self.path = self.findPathToPacman(state)
            self.path_computed = True
            self.current_path_index = 0
            
            # Print metrics after path computation
            if not self.metrics_printed:
                self.printMetrics()
            
            # Visualize the computed path
            self.visualizePath(state)
        
        # Follow the computed path
        if self.path and self.current_path_index < len(self.path):
            action = self.path[self.current_path_index]
            self.current_path_index += 1
            return action
        
        # Fallback if path is empty or exhausted
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution(dist)
    
    def visualizePath(self, state):
        """
        Visualize the computed path clearly before the ghost starts moving.
        """
        # This method can be enhanced with specific visualization code
        # For now, we'll just draw the expanded cells for reference
        self.drawExpandedCells()
        
        # Optional: can be extended to draw a clear path on the game board
        # using a different color or visualization technique
    
    def getDistribution(self, state):
        """
        Gets distribution over actions. This method should be overridden by
        subclasses to implement specific search algorithms.
        """
        util.raiseNotDefined()
        
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
    
    def findPathToPacman(self, state):
        """Simple path that tries to go left whenever possible."""
        path = []
        ghostPos = state.getGhostPosition(self.index)
        pacmanPos = state.getPacmanPosition()
        
        # This is a placeholder - in a real implementation, 
        # you would use your search algorithm here
        # For the LeftMoveOnlyGhost, we'll just return a simple path
        legalActions = state.getLegalActions(self.index)
        if Directions.WEST in legalActions:
            path.append(Directions.WEST)
        elif len(legalActions) > 0 and Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)
            if legalActions:
                path.append(random.choice(legalActions))
                
        return path

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
    
    def findPathToPacman(self, state):
        """Simple path that tries to go right whenever possible."""
        path = []
        ghostPos = state.getGhostPosition(self.index)
        pacmanPos = state.getPacmanPosition()
        
        # This is a placeholder - in a real implementation, 
        # you would use your search algorithm here
        # For the RightMoveOnlyGhost, we'll just return a simple path
        legalActions = state.getLegalActions(self.index)
        if Directions.EAST in legalActions:
            path.append(Directions.EAST)
        elif len(legalActions) > 0 and Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)
            if legalActions:
                path.append(random.choice(legalActions))
                
        return path