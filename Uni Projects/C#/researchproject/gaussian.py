import time
import random
from memory_profiler import profile

def generate_random_matrix(rows, columns):
    matrix = []
    for _ in range(rows):
        row = [random.randint(1, 100) for _ in range(columns)]
        matrix.append(row)
    return matrix

rows = 100
columns = 101
random_matrix = generate_random_matrix(rows, columns)

class GaussianElimination:
    def __init__(self, matrix):
        self.matrix = matrix

    @profile
    def eliminate(self):
        n = len(self.matrix)

        for i in range(n):
            pivot = self.matrix[i][i]

            for j in range(i + 1, n):
                factor = self.matrix[j][i] / pivot

                for k in range(i, n + 1):
                    self.matrix[j][k] -= self.matrix[i][k] * factor

    @profile
    def solve(self):
        self.eliminate()

        n = len(self.matrix)
        solution = [0] * n

        for i in range(n - 1, -1, -1):
            solution[i] = self.matrix[i][n] / self.matrix[i][i]

            for j in range(i - 1, -1, -1):
                self.matrix[j][n] -= self.matrix[j][i] * solution[i]

        return solution

@profile
def gaussian_elimination(matrix):
    n = len(matrix)

    for i in range(n):
        pivot = matrix[i][i]

        for j in range(i + 1, n):
            factor = matrix[j][i] / pivot

            for k in range(i, n + 1):
                matrix[j][k] -= matrix[i][k] * factor

    solution = [0] * n

    for i in range(n - 1, -1, -1):
        solution[i] = matrix[i][n]

        for j in range(i + 1, n):
            solution[i] -= matrix[i][j] * solution[j]

        solution[i] /= matrix[i][i]

    return solution

start_time = time.time()
procedural = gaussian_elimination(random_matrix)
procedural_time = time.time() - start_time

start_time = time.time()
gaussian = GaussianElimination(random_matrix)
object = gaussian.solve()
object_time = time.time() - start_time

#print("Procedural Gaussian Elimination Solution:", procedural)
#print("Object-Oriented Gaussian Elimination Solution:", object)
print("Procedural Execution Time:", procedural_time)
print("Object-Oriented Execution Time:", object_time)