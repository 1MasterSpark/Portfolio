from SearchAlgorithm import SearchAlgorithm
import heapq

class LongestPathSearch(SearchAlgorithm): # Tries to find the longest non-self-intersecting path to the goal. Very inefficient and does not work well
    def search(self):
        visited = set()
        frontier = [(0, self.robot.initial_state, [])]
        longest_path = []
        heapq.heapify(frontier)

        while frontier:
            _, current_state, path = heapq.heappop(frontier)
            visited.add(current_state)
            self.robot.number_of_nodes +=1
            path.append(current_state)
            if len(path) > 50:
                return longest_path, visited
            if len(path) > len(longest_path) and current_state in self.robot.goals:
                longest_path = path.copy()
            successors = self.robot.get_successors(current_state)
            for successor in successors:
                penalty = 0
                if successor in visited:
                    penalty = 5
                heapq.heappush(frontier, (penalty, successor, path.copy()))
        return None, None