import abc


class Entity(abc.ABC):

    @abc.abstractmethod
    def compute_next(self):
        raise NotImplementedError('users must define compute_next to use this base class')

    @abc.abstractmethod
    def apply_next(self):
        raise NotImplementedError('users must define apply_next to use this base class')