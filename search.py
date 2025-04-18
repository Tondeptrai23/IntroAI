from game import Actions, Directions, Configuration
from pacman import GameState
from searchAgents import SearchGhostAgent
from util import PriorityQueue, manhattanDistance
import util


class BFSGhost(SearchGhostAgent):
    """Ghost that uses Breadth-First Search (BFS) to choose actions."""
    
    def getDistribution(self, state):
        """
        Implement BFS to determine the action distribution.
        """
        # TODO: Implement BFS algorithm here
        # Example structure:
        # 1. Initialize a queue with the starting state
        # 2. While the queue is not empty:
        #    a. Dequeue the next state
        #    b. If it's the goal state, return the path
        #    c. Otherwise, enqueue its successors
        #    d. Track visited states to avoid revisiting
        pass

class DFSGhost(SearchGhostAgent):
    """Ghost that uses Depth-First Search (DFS) to choose actions."""
    
    def getDistribution(self, state):
        """
        Implement DFS to determine the action distribution.
        """
        # TODO: Implement DFS algorithm here
        # Example structure:
        # 1. Initialize a stack with the starting state
        # 2. While the stack is not empty:
        #    a. Pop the next state
        #    b. If it's the goal state, return the path
        #    c. Otherwise, push its successors onto the stack
        #    d. Track visited states to avoid revisiting
        pass

class UCSGhost(SearchGhostAgent):
    """Ghost that uses Uniform-Cost Search (UCS) to choose actions."""
    
    def getDistribution(self, state):
        """
        Implement UCS to determine the action distribution.
        """
        # TODO: Implement UCS algorithm here
        # Example structure:
        # 1. Initialize a priority queue with the starting state and cost 0
        # 2. While the queue is not empty:
        #    a. Dequeue the state with the lowest cost
        #    b. If it's the goal state, return the path
        #    c. Otherwise, enqueue its successors with updated costs
        #    d. Track visited states and their costs to avoid revisiting with higher cost
        pass

class AStarGhost(SearchGhostAgent):
    """Ghost that uses A* Search to choose actions."""

    def getDistribution(self, state: GameState):
        """
        Implement A* Search to determine the action distribution.
        """
        if (len(state.getLegalActions(self.index)) == 1):
            dist = util.Counter()
            dist[state.getLegalActions(self.index)[0]] = 1.0
            return dist

        startPosition = state.getGhostPosition(self.index)
        pacmanPosition = state.getPacmanPosition()
        walls = state.getWalls()

        frontier = PriorityQueue()
        frontier.push((startPosition, []), 0)  
        visited = set()

        while not frontier.isEmpty():
            currentPosition, path = frontier.pop()

            if currentPosition == pacmanPosition:
                dist = util.Counter()
                if path:
                    dist[path[0]] = 1.0 
                return dist
            
            if currentPosition in visited:
                continue
            visited.add(currentPosition)

            if currentPosition == startPosition:
                legalActions = state.getLegalActions(self.index) 
            else:
                legalActions = Actions.getPossibleActions(
                    Configuration(currentPosition, Directions.STOP), walls
                )
            for action in legalActions:
                dx, dy = Actions.directionToVector(action)
                nextPosition = (int(currentPosition[0] + dx), int(currentPosition[1] + dy))

                newPath = path + [action]
                g = len(newPath)  
                h = manhattanDistance(nextPosition, pacmanPosition)  
                f = g + h

                frontier.push((nextPosition, newPath), f)

        dist = util.Counter()
        dist[Directions.STOP] = 1.0
        return dist