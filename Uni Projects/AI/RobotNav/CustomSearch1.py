from SearchAlgorithm import SearchAlgorithm

class BeamSearch(SearchAlgorithm):
    def search(self, beam_width=10):
        visited = set()
        frontier = [(self.robot.initial_state, [])]

        while frontier:
            next_frontier = [] # Pretty much same as BFS
            for current_state, path in frontier:
                if current_state in visited:
                    continue
                visited.add(current_state)
                self.robot.number_of_nodes += 1
                path.append(current_state)
                if current_state in self.robot.goals:
                    return path, visited
                successors = self.robot.get_successors(current_state)
                for successor in successors:
                    next_frontier.append((successor, path.copy()))
            next_frontier.sort(key=lambda x: self.robot.heuristic(x[0])) # Order the frontier by heuristic
            frontier = next_frontier[:beam_width] # Only add to the next frontier the best 10 successors
        return None, None