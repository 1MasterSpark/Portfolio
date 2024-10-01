from SearchAlgorithm import SearchAlgorithm

class DepthFirstSearch(SearchAlgorithm):
    def search(self):
        visited = set()
        frontier = [(self.robot.initial_state, [])] # Create a queue

        while frontier:
            current_state, path = frontier.pop() # Take the last position added to the queue and remove it from the queue
            if current_state in visited:
                continue
            visited.add(current_state)
            self.robot.number_of_nodes += 1
            path.append(current_state)
            if current_state in self.robot.goals:
                return path, visited
            successors = self.robot.get_successors(current_state)
            successors.reverse() # The frontier is LIFO so this ensures that the next successor is by default up, then left, then down, then right
            for successor in successors:
                frontier.append((successor, path.copy()))
        return None, None