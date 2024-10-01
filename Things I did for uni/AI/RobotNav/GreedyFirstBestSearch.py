from SearchAlgorithm import SearchAlgorithm
import heapq

class GreedyBestFirstSearch(SearchAlgorithm):
    def search(self):
        visited = set()
        frontier = [(self.robot.heuristic(self.robot.initial_state), self.robot.initial_state, [])]
        heapq.heapify(frontier) # A heap can be ordered by some heuristic

        while frontier:
            _, current_state, path = heapq.heappop(frontier) # Take the last (most optimal) state in the frontier
            if current_state in visited:
                continue
            visited.add(current_state)
            self.robot.number_of_nodes +=1
            path.append(current_state)
            if current_state in self.robot.goals:
                return path, visited
            successors = self.robot.get_successors(current_state)
            for successor in successors:
                heapq.heappush(frontier, (self.robot.heuristic(successor), successor, path.copy())) # Add them to the frontier sorted by heuristic (Manhattan distance to nearest goal)
        return None, None