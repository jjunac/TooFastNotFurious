from engine.state import State


class Entity:

    def __init__(self, length, transitions):
        self.length = length
        self.transitions = transitions
        self.cells = [State.EMPTY] * length

    def tick(self):
        next = [0] * self.length
        for i in range(self.length):
            next[i] = self.transitions.get([self.get_state(i - 1), self.get_state(i), self.get_state(i + 1)])
        self.cells = next

    def get_state(self, i):
        if 0 <= i < self.length:
            return self.cells[i]
        else:
            return State.EMPTY