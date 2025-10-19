import math
import time
from memory_profiler import profile

@profile
def integrate_procedural(f, a, b, n):
    dx = (b - a) / n
    total_area = 0

    for i in range(n):
        x = a + i * dx
        height = f(x)
        area = height * dx
        total_area += area

    return total_area

class Integrator:
    def __init__(self, f, a, b, n):
        self.f = f
        self.a = a
        self.b = b
        self.n = n

    @profile
    def integrate(self):
        dx = (self.b - self.a) / self.n
        total_area = 0

        for i in range(self.n):
            x = self.a + i * dx
            height = self.f(x)
            area = height * dx
            total_area += area

        return total_area
    
def function(x):
    return (math.sin(x) ** 2) + math.sqrt(abs(x)) + math.exp(x) - math.log(x + 1)

a = 0
b = 100
n = 10000

start_time = time.time()
result_procedural = integrate_procedural(function, a, b, n)
#print("Procedural Integration Result:", result_procedural)
procedural_time = time.time() - start_time

start_time = time.time()
integrator = Integrator(function, a, b, n)
result_object_oriented = integrator.integrate()
#print("Object-Oriented Integration Result:", result_object_oriented)
object_time = time.time() - start_time

print("Procedural Execution Time:", procedural_time)
print("Object-Oriented Execution Time:", object_time)