import sys
import tkinter as tk
from DepthFirstSearch import DepthFirstSearch
from BreadthFirstSearch import BreadthFirstSearch
from GreedyFirstBestSearch import GreedyBestFirstSearch
from AStarSearch import AStarSearch
from CustomSearch1 import BeamSearch
from CustomSearch2 import IterativeDeepeningAStarSearch
from LongestPathSearch import LongestPathSearch
from GUI import GUI
from Robot import Robot

def read_problem_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        grid_size = eval(lines[0]) # First line is the grid size
        initial_state = eval(lines[1]) # Second line is intial state
        goals = set(eval(goal) for goal in lines[2].split("|")) # Third line is goals
        walls = set()
        for line in lines[3:]: # Remaining lines are walls
            if "(" in line:
                x, y, w, h = eval(line)
                for i in range(w):
                    for j in range(h):
                        walls.add((x + i, y + j))

    return grid_size, initial_state, goals, walls

def get_directions(path): # Converts an array of coordinates to an array of directions so the output matches the instructions
    directions = []
    for i in range(1, len(path)):
        prev_x, prev_y = path[i-1]
        curr_x, curr_y = path[i]
        if curr_x == prev_x:
            if curr_y > prev_y:
                directions.append("down")
            else:
                directions.append("up")
        else:
            if curr_x > prev_x:
                directions.append("right")
            else:
                directions.append("left")
    return directions

def main():
    if len(sys.argv) < 3:
        print("Error: Invalid input")
        print("Usage: python search.py <filename> <method> [gui]")
        sys.exit(1)
    
    filename = sys.argv[1]
    method = sys.argv[2]
    method = method.lower()
    grid_size, initial_state, goals, walls = read_problem_file(filename)
    robot = Robot(grid_size, initial_state, goals, walls)
    algorithm = None

    if method == "dfs":
        algorithm = DepthFirstSearch(robot)
        print(filename, "DFS")
    elif method == "bfs":
        algorithm = BreadthFirstSearch(robot)
        print(filename, "BFS")
    elif method == "gbfs":
        algorithm = GreedyBestFirstSearch(robot)
        print(filename, "GBFS")
    elif method == "as":
        algorithm = AStarSearch(robot)
        print(filename, "AS")
    elif method == "cus1":
        algorithm = BeamSearch(robot)
        print(filename, "CUS1")
    elif method == "cus2":
        algorithm = IterativeDeepeningAStarSearch(robot)
        print(filename, "CUS2")
    elif method == "lps":
        algorithm = LongestPathSearch(robot)
        print(filename, "LPS")
    else:
        print("Error: Invalid method")

    if algorithm:
        path, visited = algorithm.search()
        if path:
            print("<Node ", str(path[-1]) + ">", robot.number_of_nodes)
            print(get_directions(path))
        else:
            print("No goal is reachable;", robot.number_of_nodes)

        if len(sys.argv) > 3 and sys.argv[3].lower() == "gui":
            root = tk.Tk()
            gui = GUI(root, robot, path, visited)
            root.mainloop()

if __name__ == "__main__":
    main()