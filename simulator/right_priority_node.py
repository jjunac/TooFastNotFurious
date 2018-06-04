from simulator.abstract_node import AbstractNode


class RightPriorityNode(AbstractNode):
    def __init__(self):
        AbstractNode.__init__(self)
        self.priority = None

    def can_move(self, node):

        if self.next_car or self.current_car:
            return False

        if self.priority:
            return node == self.priority

        predecessor_with_car = list(filter(lambda x: x.current_car, self.predecessors))

        car_with_right_priority = list(filter(self.__has_right_priority, predecessor_with_car))
        if len(car_with_right_priority) == 1:
            self.priority = car_with_right_priority[0]
            return node == self.priority

        car_that_dont_cross_opposite = list(filter(self.__dont_have_to_cross_opposite_car_way, self.predecessors))
        # If there is only one, we return the only one
        # If not, we pick a car that goes first (so why not the first one)
        if car_that_dont_cross_opposite:
            self.priority = car_that_dont_cross_opposite[0]
            return node == self.priority

        # If they all have to cross, let's pick one (so why not the first one)
        self.priority = car_with_right_priority[0]
        return node == self.priority


    def apply_next(self):
        super().apply_next()
        self.priority = None

    def __has_right_priority(self, node):
        priority = self.__get_predecessor_from_orientation(node.orientation.left())
        return not priority or not priority.current_car

    def __get_predecessor_from_orientation(self, orientation):
        res = list(filter(lambda s: s.orientation == orientation, self.predecessors))
        return res[0] if res else None

    def __dont_have_to_cross_opposite_car_way(self, node):
        destination_node = self.successors[node.current_car.path.directions[1]]
        if node.orientation.left() == destination_node.orientation or node.orientation.invert() == destination_node.orientation:
            # If the car will cross the opposite road, check if there is someone
            opposite = self.__get_predecessor_from_orientation(node.orientation.invert())
            if opposite and opposite.current_car:
                return False
        return True
