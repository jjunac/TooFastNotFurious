class TransitionTable:
    def __init__(self, dimension, initial_value=0):
        self.dimension = dimension
        self.transitions = initial_value
        for _ in range(dimension):
            self.transitions = [self.transitions] * dimension

    def set(self, indexes, value):
        self.__check_dimension(indexes)
        tmp = self.transitions
        for i in indexes[:-1]:
            tmp = tmp[i]
        tmp[indexes[-1]] = value

    def get(self, indexes):
        self.__check_dimension(indexes)
        tmp = self.transitions
        for i in indexes:
            tmp = tmp[i]
        return tmp

    def __check_dimension(self, indexes):
        if len(indexes) != self.dimension:
            raise IndexError('Number of arguments must be equal to the dimension of the table: %d' % self.dimension)
