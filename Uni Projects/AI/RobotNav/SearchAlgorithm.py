class SearchAlgorithm: # Abstact class for search algorithms
    def __init__(self, robot):
        self.robot = robot

    def search(self):
        raise NotImplementedError