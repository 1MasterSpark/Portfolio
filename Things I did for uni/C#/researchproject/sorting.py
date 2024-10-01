import time
import random
from memory_profiler import profile

@profile
def bubble_sort_procedural(arr):
    n = len(arr)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr

class BubbleSort:
    def __init__(self, arr):
        self.arr = arr

    @profile
    def sort(self):
        n = len(self.arr)

        for i in range(n - 1):
            for j in range(n - 1 - i):
                if self.arr[j] > self.arr[j + 1]:
                    self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]

        return self.arr

array = [random.randint(1, 1000) for i in range(1000)]

start_time = time.time()
bubble = BubbleSort(array)
array_object_oriented = bubble.sort()
#print("Object-Oriented Sorted Array:", array_object_oriented)
object_time = time.time() - start_time

start_time = time.time()
array_procedural = bubble_sort_procedural(array)
#print("Procedural Sorted Array:", array_procedural)
procedural_time = time.time() - start_time

print("Procedural Execution Time:", procedural_time)
print("Object-Oriented Execution Time:", object_time)