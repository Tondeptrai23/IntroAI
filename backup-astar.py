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