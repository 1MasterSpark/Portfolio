import time
import math
from memory_profiler import profile

@profile
def newton_procedural(f, f_prime, initial_guess, max_iterations=10000):
    x = initial_guess
    iteration = 0

    while iteration < max_iterations:
        x = x - f(x) / f_prime(x)
        iteration += 1

    return x

class NewtonMethod:
    def __init__(self, f, f_prime, initial_guess, max_iterations=10000):
        self.f = f
        self.f_prime = f_prime
        self.initial_guess = initial_guess
        self.max_iterations = max_iterations

    @profile
    def find_root(self):
        x = self.initial_guess
        iteration = 0

        while iteration < self.max_iterations:
            x = x - self.f(x) / self.f_prime(x)
            iteration += 1

        return x
        
def function(x):
    return (math.sin(x) ** 2) + math.sqrt(x) + math.exp(x) - math.log(x + 1) - 3

def function_prime(x):
    return 2 * math.sin(x) * math.cos(x) + 0.5 * math.sqrt(x) + math.exp(x) - 1/(x + 1)

initial_guess = 1.5

start_time = time.time()
root_procedural = newton_procedural(function, function_prime, initial_guess)
print("Procedural Root:", root_procedural)
procedural_time = time.time() - start_time

start_time = time.time()
newton = NewtonMethod(function, function_prime, initial_guess)
root_object_oriented = newton.find_root()
print("Object-Oriented Root:", root_object_oriented)
object_time = time.time() - start_time

print("Procedural Execution Time:", procedural_time)
print("Object-Oriented Execution Time:", object_time)