from modeler.entry_node import EntryNode
from modeler.exit_node import ExitNode
from modeler.right_priority_junction import RightPriorityJunction
from modeler.simulation import Simulation
from modeler.stop_junction import StopJunction
from modeler.traffic_light import TrafficLight
from modeler.roundabout import Roundabout

nodes = []


def entry_node():
    node = EntryNode()
    nodes.append(node)
    return node


def exit_node():
    node = ExitNode()
    nodes.append(node)
    return node


def new_simulation():
    return Simulation()


def right_priority():
    return RightPriorityJunction()


def traffic_light():
    return TrafficLight()


def stop():
    return StopJunction()

def roundabout():
    return Roundabout()