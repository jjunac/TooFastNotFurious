from engine.entity import Entity
from engine.state import State
from engine.transition_table import TransitionTable

class Road(Entity):

    transitions = TransitionTable(3)
    transitions.set([State.EMPTY,   State.EMPTY,    State.EMPTY],   State.EMPTY)
    transitions.set([State.EMPTY,   State.EMPTY,    State.CAR],     State.EMPTY)
    transitions.set([State.EMPTY,   State.CAR,      State.EMPTY],   State.EMPTY)
    transitions.set([State.EMPTY,   State.CAR,      State.CAR],     State.CAR)
    transitions.set([State.CAR,     State.EMPTY,    State.EMPTY],   State.CAR)
    transitions.set([State.CAR,     State.EMPTY,    State.CAR],     State.CAR)
    transitions.set([State.CAR,     State.CAR,      State.EMPTY],   State.EMPTY)
    transitions.set([State.CAR,     State.CAR,      State.CAR],     State.CAR)


    def __init__(self, length):
        self.cells = [State.EMPTY] * length
        self.length = length
        self.next = [0] * self.length


    def compute_next(self):
        self.reset_next()
        for i in range(self.length):
            self.set_next_state(i, self.transitions.get([self.get_state(i-1), self.get_state(i), self.get_state(i+1)]))


    def apply_next(self):
        self.cells = self.next



    def get_state(self, i):
        if 0 <= i < self.length:
            return self.cells[i]
        else:
            return State.EMPTY

    def reset_next(self):
        self.next = [0] * self.length

    def set_next_state(self, i, value):
        self.next[i] = value
