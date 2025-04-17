from searchAgents import SearchGhostAgent


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
    
    def getDistribution(self, state):
        """
        Implement A* Search to determine the action distribution.
        """
        # TODO: Implement A* algorithm here
        # Example structure:
        # 1. Initialize a priority queue with the starting state and cost 0 + heuristic
        # 2. While the queue is not empty:
        #    a. Dequeue the state with the lowest cost + heuristic
        #    b. If it's the goal state, return the path
        #    c. Otherwise, enqueue its successors with updated costs + heuristics
        #    d. Track visited states and their costs to avoid revisiting with higher cost
        pass
