from SearchAlgorithm import SearchAlgorithm
from collections import deque

class BreadthFirstSearch(SearchAlgorithm):
    def search(self):
        visited = set()
        frontier = deque([(self.robot.initial_state, [])]) # Deque creates a double-ended queue

        while frontier:
            current_state, path = frontier.popleft() # Take the leftmost (oldest) state in the queue and remove it form the queue
            if current_state in visited:
                continue
            visited.add(current_state)
            self.robot.number_of_nodes += 1
            path.append(current_state)
            if current_state in self.robot.goals:
                return path, visited
            successors = self.robot.get_successors(current_state)
            for successor in successors:
                frontier.append((successor, path.copy())) # Add all the successors to the queue
        return None, None