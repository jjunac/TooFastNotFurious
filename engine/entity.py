import abc


class Entity(abc.ABC):

    @abc.abstractmethod
    def tick(self):
        raise NotImplementedError('users must define tick to use this base class')

    @abc.abstractmethod
    def get_state(self, i):
        raise NotImplementedError('users must define get_state to use this base class')
