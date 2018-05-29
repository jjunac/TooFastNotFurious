from engine.tickable import Tickable
from engine.state import State
from engine.transition_table import TransitionTable

class Road(Tickable):

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


    def tick(self):
        next = [0] * self.length
        for i in range(self.length):
            next[i] = self.transitions.get([self.get_state(i-1), self.get_state(i), self.get_state(i+1)])
        self.cells = next

    def get_state(self, i):
        if 0 <= i < self.length:
            return self.cells[i]
        else:
            return State.EMPTY

