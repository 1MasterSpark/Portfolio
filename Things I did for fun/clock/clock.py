import time

class Counter:
    def __init__(self, name):
        self._count = 0
        self._name = name

    def increment(self):
        self._count += 1

    def reset(self):
        self._count = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def ticks(self):
        return self._count


class Clock:
    def __init__(self):
        self._seconds = Counter("seconds")
        self._minutes = Counter("minutes")
        self._hours = Counter("hours")

    def tick(self):
        self._seconds.increment()
        if self._seconds.ticks == 60:
            self._seconds.reset()
            self._minutes.increment()
            if self._minutes.ticks == 60:
                self._minutes.reset()
                self._hours.increment()
                if self._hours.ticks == 24:
                    self.reset_all()

    def reset_all(self):
        self._seconds.reset()
        self._minutes.reset()
        self._hours.reset()

    def time(self):
        return [self._hours.ticks, self._minutes.ticks, self._seconds.ticks]


clock = Clock()

while True:
    clock.tick()
    current_time = clock.time()
    print(f"Time: {current_time[0]:02d}:{current_time[1]:02d}:{current_time[2]:02d}")
    time.sleep(1)

# Ctrl C to quit