from SearchAlgorithm import SearchAlgorithm
import heapq

class IterativeDeepeningAStarSearch(SearchAlgorithm):
    def search(self, max_depth=12):
        for depth in range(max_depth): # If max depth is 10 or less, the algorithm with not find a solution
            path, visited = self.depth_limited_astar(depth)
            if path and visited:
                return path, visited
        return None, None

    def depth_limited_astar(self, max_depth):
        visited = set()
        g_scores = {self.robot.initial_state: 0}
        frontier = [(self.robot.heuristic(self.robot.initial_state), self.robot.initial_state, [])]
        heapq.heapify(frontier)

        while frontier:
            _, current_state, path = heapq.heappop(frontier)
            if len(path) > max_depth:
                continue
            if current_state in visited:
                continue
            visited.add(current_state)
            self.robot.number_of_nodes += 1
            path.append(current_state)
            if current_state in self.robot.goals:
                return path, visited
            successors = self.robot.get_successors(current_state)
            for successor in successors:
                new_g_score = g_scores[current_state] + 1
                if successor not in g_scores or new_g_score < g_scores[successor]:
                    g_scores[successor] = new_g_score
                    heapq.heappush(frontier, (new_g_score + self.robot.heuristic(successor), successor, path.copy()))
        return None, None # Exact same as A*. But the depth limit makes it more memory efficient because it doesn't store the entire search tree in memory