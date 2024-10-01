from SearchAlgorithm import SearchAlgorithm
import heapq

class AStarSearch(SearchAlgorithm):
    def search(self):
        visited = set()
        g_scores = {self.robot.initial_state: 0}
        frontier = [(self.robot.heuristic(self.robot.initial_state), self.robot.initial_state, [])]
        heapq.heapify(frontier) # Same as GBFS

        while frontier:
            _, current_state, path = heapq.heappop(frontier)
            if current_state in visited:
                continue
            visited.add(current_state)
            self.robot.number_of_nodes +=1
            path.append(current_state)
            if current_state in self.robot.goals:
                return path, visited
            successors = self.robot.get_successors(current_state)
            for successor in successors:
                new_g_score = g_scores[current_state] + 1 # The g-score of a successor is the cost of reaching it, which is 1 + the g-score of the current state
                if successor not in g_scores or new_g_score < g_scores[successor]:
                    g_scores[successor] = new_g_score
                    heapq.heappush(frontier, (new_g_score + self.robot.heuristic(successor), successor, path.copy())) # Order the frontier by h(n) + g(n)
        return None, None