import tkinter as tk

class GUI:
    def __init__(self, master, robot, path, visited):
        self.master = master
        self.robot = robot
        self.path = path
        self.visited = visited
        self.canvas = None
        self.delay = 500  # Delay in milliseconds

        self.setup_gui()
        self.setup_environment()
        self.visualize_search()

    def setup_gui(self):
        self.master.title("RobotNav")

        self.canvas = tk.Canvas(self.master, width=(self.robot.grid_size[1] * 50),
                                height=(self.robot.grid_size[0] * 50), bg="white") # Dimensions of window = 50 * grid size
        self.canvas.pack()

    def setup_environment(self):
        robot = self.robot
        for y in range(robot.grid_size[0]):
            for x in range(robot.grid_size[1]):
                if (x, y) == robot.initial_state:
                    color = "red"  # Initial state
                elif (x, y) in robot.goals:
                    color = "lightgreen"  # Goals
                elif (x, y) in robot.walls:
                    color = "grey"  # Wall
                elif (x, y) in self.visited:
                    color = "lightblue"  # Visited
                else:
                    color = "white"  # Empty space
                self.canvas.create_rectangle(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill=color)

    def visualize_search(self, index=0):
        if self.path and self.visited:
            if index < len(self.path) - 1:
                x1, y1 = self.path[index]
                x2, y2 = self.path[index + 1]
                self.canvas.create_line(x1 * 50 + 25, y1 * 50 + 25, x2 * 50 + 25, y2 * 50 + 25, fill="red")
                self.master.after(self.delay, self.visualize_search, index + 1) # Short delay. Creates illusion of watching the algorithm in action