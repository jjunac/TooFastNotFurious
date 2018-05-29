import abc


class Tickable(abc.ABC):

    @abc.abstractmethod
    def tick(self):
        raise NotImplementedError('users must define tick to use this base class')
