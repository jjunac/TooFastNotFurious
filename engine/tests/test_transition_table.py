import unittest

from engine.transition_table import TransitionTable


class TestTransitionTable(unittest.TestCase):

    def test_should_create_the_right_dimension_when_create_table(self):
        t = TransitionTable(3)
        t.get([0, 0, 0])
        t.get([2, 2, 2])
        with self.assertRaises(IndexError):
            t.get([3, 3, 3])

    def test_should_initialize_the_table_with_the_initial_value_when_create_table(self):
        t = TransitionTable(2, 42)
        self.assertEqual(42, t.get([0, 0]))
        self.assertEqual(42, t.get([0, 1]))
        self.assertEqual(42, t.get([1, 0]))
        self.assertEqual(42, t.get([1, 1]))

    def test_should_verify_dimension_when_get(self):
        t = TransitionTable(3)
        with self.assertRaises(IndexError):
            t.get([1, 1, 1, 1])

    def test_should_set_value_when_set(self):
        t = TransitionTable(2)
        t.set([1, 1], 5)
        self.assertEqual(0, t.get([0, 0]))
        self.assertEqual(0, t.get([0, 1]))
        self.assertEqual(0, t.get([1, 0]))
        self.assertEqual(5, t.get([1, 1]))

