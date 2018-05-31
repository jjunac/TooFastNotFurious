from collections import deque


class Path:

    def __init__(self, directions):
        self.directions = deque(directions)


    def next_direction(self):
        return self.directions[0]


    def pop_direction(self):
        return self.directions.popleft()
