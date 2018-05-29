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
        super().__init__(length, self.transitions)

