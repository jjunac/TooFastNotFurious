# Algorithms & Data Structures
# SI3 - Polytech Nice-Sophia - Edition 2018
# Python 3.6
# by Christophe Papazian
# modified by Marc Gaetano

class DijkstraHeap:

    def __init__(self):
        self._array = []
        self._locator = {}

    def _left(self, n):
        return 2 * n + 1

    def _right(self, n):
        return 2 * n + 2

    def _parent(self, n):
        return (n - 1) // 2

    def __getitem__(self, n):
        return self._array[n]

    def __setitem__(self, n, v):
        self._array[n] = v

    def __len__(self):
        return len(self._array)

    def __bool__(self):
        return bool(self._array)

    def __repr__(self):
        return repr(self._array)

    def smaller(self, i, j):
        return i < len(self._array) and j < len(self._array) and self._array[i] < self._array[j]

    def percolate_down(self, n):
        '''
        move the element at index n down in the tree at the right place.
        '''
        while True:
            if self.smaller(self._left(n), n) and not self.smaller(self._right(n), self._left(n)):
                nxt = self._left(n)
            elif self.smaller(self._right(n), n):
                nxt = self._right(n)
            else:
                return n
            self[n], self[nxt] = self[nxt], self[n]
            self._locator[self[n]] = n
            self._locator[self[nxt]] = nxt
            n = nxt

    def percolate_up(self, n):
        '''
        move the element at index n up in the tree at the right place.
        '''
        while n > 0:
            if self.smaller(n, self._parent(n)):
                self[n], self[self._parent(n)] = self[self._parent(n)], self[n]
                self._locator[self[n]] = n
                self._locator[self[self._parent(n)]] = self._parent(n)
                n = self._parent(n)
            else:
                return n

    def pop(self):
        '''
        return the extremum element and remove it from the heap.
        '''
        if len(self) == 0: raise ValueError("BinaryHeap.pop on empty heap")
        if len(self) == 1: return self._array.pop()
        v, self[0] = self[0], self._array.pop()
        self._locator[self[0]] = 0
        self.percolate_down(0)
        return v

    def add(self, v):
        '''
        add the element v on the heap.
        '''
        self._array.append(v)
        self._locator[v] = len(self) - 1
        self.percolate_up(len(self) - 1)

    def decreaseKey(self, v):
        '''
        rearrange v
        '''
        self.percolate_up(self._locator[v])