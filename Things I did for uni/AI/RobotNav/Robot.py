class Robot:
    def __init__(self, grid_size, initial_state, goals, walls):
        self.grid_size = grid_size
        self.initial_state = initial_state
        self.goals = goals
        self.walls = walls
        self.number_of_nodes = 0 # This keeps track of the number of nodes visited

    def move(self, current_state, dx, dy): # Originally I had four functions (moveleft, moveright, moveup, movedown) but I realised one function could do it
        x, y = current_state
        new_x, new_y = x + dx, y + dy
        
        if 0 <= new_x < self.grid_size[1] and 0 <= new_y < self.grid_size[0]:
            if (new_x, new_y) not in self.walls: # Destination has to be within the grid and not in a wall
                return (new_x, new_y)
        return None
    
    def get_successors(self, current_state):
        dx = [0, -1, 0, 1]
        dy = [-1, 0, 1, 0] # Up, left, down, right
        successors = []
        for i in range(4):
            new_state = self.move(current_state, dx[i], dy[i])
            if new_state:
                successors.append(new_state)
        return successors
    
    def heuristic(self, state):
        min_distance = float('inf')
        for goal in self.goals:
            distance = abs(goal[0] - state[0]) + abs(goal[1] - state[1])
            min_distance = min(min_distance, distance) # Manhattan distance to nearest goal
        return min_distance