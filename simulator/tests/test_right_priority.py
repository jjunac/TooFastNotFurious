import unittest

from shared import Orientation
from simulator import Road, Simulator
from simulator.car import Car
from simulator.path import Path
from simulator.right_priority_junction import RightPriorityJunction
from simulator.utils import *
from copy import deepcopy


class TestRightPriority(unittest.TestCase):

    def test_should_go_when_there_is_no_right_priority(self):
        simulator = Simulator()
        rp = RightPriorityJunction(simulator, 1, 1)
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.EAST, 1)
        r1.nodes[0][0].current_car = Car(Path([rp.nodes[0][0], r3.nodes[0][0]]), r1.nodes[0][0])
        r2.nodes[0][0].current_car = Car(Path([rp.nodes[0][0], r3.nodes[0][0]]), r2.nodes[0][0])

        rp.add_predecessor(Orientation.NORTH, r1)
        rp.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.EAST, rp)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)

    def test_should_go_when_there_is_right_priority_and_no_car_present(self):
        simulator = Simulator()
        rp = RightPriorityJunction(simulator, 1, 1)
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.EAST, 1)
        r1.nodes[0][0].current_car = Car(Path([rp.nodes[0][0], r3.nodes[0][0]]), r1)

        rp.add_predecessor(Orientation.NORTH, r1)
        rp.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.EAST, rp)

        simulator.tick()

        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

    def test_should_not_go_when_there_is_someone_in_junction_and_no_one_in_priority_road(self):
        simulator = Simulator()
        rp = RightPriorityJunction(simulator, 1, 1)
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.EAST, 1)
        r1.nodes[0][0].current_car = Car(Path([rp.nodes[0][0], r3.nodes[0][0]]), r1)
        rp.nodes[0][0].current_car = Car(Path([r3.nodes[0][0]]), rp)

        rp.add_predecessor(Orientation.NORTH, r1)
        rp.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.EAST, rp)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)

    def test_should_respect_right_priority_when_there_are_3_inputs_and_an_exit_with_double_way_road(self):
        simulator = Simulator()
        rp = RightPriorityJunction(simulator, 1, 1)
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.SOUTH, 1)
        r4 = Road(simulator, 1, Orientation.EAST, 1)

        p = Path([rp.nodes[0][0], r4.nodes[0][0]])
        r1.nodes[0][0].current_car = Car(p, r1)
        r2.nodes[0][0].current_car = Car(p, r2)
        r3.nodes[0][0].current_car = Car(p, r3)

        rp.add_predecessor(Orientation.NORTH, r1)
        rp.add_predecessor(Orientation.WEST, r2)
        rp.add_predecessor(Orientation.SOUTH, r3)
        r4.add_predecessor(Orientation.EAST, rp)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(r4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNotNone(r4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(r4.nodes[0][0].current_car)

    def test_should_respect_right_priority_when_there_are_3_inputs(self):
        simulator = Simulator()
        rp = RightPriorityJunction(simulator, 1, 1)
        entryN = Road(simulator, 1, Orientation.NORTH, 1)
        entryW = Road(simulator, 1, Orientation.WEST, 1)
        entryS = Road(simulator, 1, Orientation.SOUTH, 1)
        exitW = Road(simulator, 1, Orientation.WEST, 1)

        p = Path([rp.nodes[0][0], exitW.nodes[0][0]])
        entryN.nodes[0][0].current_car = Car(p, entryN)
        entryW.nodes[0][0].current_car = Car(p, entryW)
        entryS.nodes[0][0].current_car = Car(p, entryS)

        rp.add_predecessor(Orientation.NORTH, entryN)
        rp.add_predecessor(Orientation.WEST, entryW)
        rp.add_predecessor(Orientation.SOUTH, entryS)
        exitW.add_predecessor(Orientation.WEST, rp)

        simulator.tick()
        self.assertIsNotNone(entryN.nodes[0][0].current_car)
        self.assertIsNotNone(entryW.nodes[0][0].current_car)
        self.assertIsNone(entryS.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(exitW.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(entryN.nodes[0][0].current_car)
        self.assertIsNotNone(entryW.nodes[0][0].current_car)
        self.assertIsNone(entryS.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNotNone(exitW.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(entryN.nodes[0][0].current_car)
        self.assertIsNone(entryW.nodes[0][0].current_car)
        self.assertIsNone(entryS.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(exitW.nodes[0][0].current_car)

    def test_should_respect_right_priority_when_there_are_2_inputs_and_2_output(self):
        simulator = Simulator()
        rp = RightPriorityJunction(simulator, 1, 1)
        entryN = Road(simulator, 1, Orientation.NORTH, 1)
        entryW = Road(simulator, 1, Orientation.WEST, 1)
        exitW = Road(simulator, 1, Orientation.WEST, 1)
        exitN = Road(simulator, 1, Orientation.NORTH, 1)

        entryW.nodes[0][0].current_car = Car(Path([rp.nodes[0][0], exitW.nodes[0][0]]), entryW)
        entryN.nodes[0][0].current_car = Car(Path([rp.nodes[0][0], exitN.nodes[0][0]]), entryN)

        rp.add_predecessor(Orientation.NORTH, entryN)
        rp.add_predecessor(Orientation.WEST, entryW)
        exitW.add_predecessor(Orientation.WEST, rp)
        exitN.add_predecessor(Orientation.NORTH, rp)

        simulator.tick()
        self.assertIsNotNone(entryN.nodes[0][0].current_car)
        self.assertIsNone(entryW.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(exitW.nodes[0][0].current_car)
        self.assertIsNone(exitN.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(entryN.nodes[0][0].current_car)
        self.assertIsNone(entryW.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNotNone(exitW.nodes[0][0].current_car)
        self.assertIsNone(exitN.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(entryN.nodes[0][0].current_car)
        self.assertIsNone(entryW.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(exitW.nodes[0][0].current_car)
        self.assertIsNone(exitN.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(entryN.nodes[0][0].current_car)
        self.assertIsNone(entryW.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNone(exitW.nodes[0][0].current_car)
        self.assertIsNotNone(exitN.nodes[0][0].current_car)

    def test_should_prioritize_the_car_on_the_left_of_the_exit_when_2_car_are_facing_each_others(self):
        simulator = Simulator()
        rp = RightPriorityJunction(simulator, 1, 1)
        entry1 = Road(simulator, 1, Orientation.EAST, 1)
        entry2 = Road(simulator, 1, Orientation.WEST, 1)
        exit = Road(simulator, 1, Orientation.NORTH, 1)
        p = Path([rp.nodes[0][0], exit.nodes[0][0]])

        entry1.nodes[0][0].current_car = Car(p, entry1)
        entry2.nodes[0][0].current_car = Car(p, entry2)

        rp.add_predecessor(Orientation.EAST, entry1)
        rp.add_predecessor(Orientation.WEST, entry2)
        exit.add_predecessor(Orientation.NORTH, rp)

        self.assertIsNotNone(entry1.nodes[0][0].current_car)
        self.assertIsNotNone(entry2.nodes[0][0].current_car)
        self.assertIsNone(exit.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(entry1.nodes[0][0].current_car)
        self.assertIsNotNone(entry2.nodes[0][0].current_car)
        self.assertIsNone(exit.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(entry1.nodes[0][0].current_car)
        self.assertIsNotNone(entry2.nodes[0][0].current_car)
        self.assertIsNotNone(exit.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(entry1.nodes[0][0].current_car)
        self.assertIsNone(entry2.nodes[0][0].current_car)
        self.assertIsNone(exit.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)

    def test_should_return_start_nodes_when_get_start_is_called(self):
        simulator = Simulator()
        dictionnary = {
            Orientation.NORTH: (3, 2),
            Orientation.EAST: (3, 2)
        }
        rp = RightPriorityJunction(simulator, dictionnary)
        self.assertEqual(len(rp.get_start(Orientation.NORTH)), 3)
        self.assertEqual(len(rp.get_start(Orientation.SOUTH)), 2)
        self.assertEqual(len(rp.get_start(Orientation.EAST)), 3)
        self.assertEqual(len(rp.get_start(Orientation.WEST)), 2)

    def test_should_create_intern_mesh_when_junction_is_created(self):
        simulator = Simulator()
        dictionnary = {
            Orientation.NORTH: (3, 2),
            Orientation.EAST: (3, 2)
        }
        rp = RightPriorityJunction(simulator, dictionnary)

        for i in range( rp.size_north_south ):
            for j in range( rp.size_east_west ):
                if i < dictionnary[Orientation.NORTH][1] :
                    if j!=0:
                        self.assertIn(rp.nodes[j-1][i], rp.nodes[j][i].successors)
                else:
                    if j != rp.size_north_south-1:
                        self.assertIn(rp.nodes[j+1][i], rp.nodes[j][i].successors)
                if j < dictionnary[Orientation.EAST][0]:
                    if i != rp.size_north_south-1:
                        self.assertIn(rp.nodes[j][i+1], rp.nodes[j][i].successors)
                else:
                    if i != 0:
                        self.assertIn(rp.nodes[j][i-1], rp.nodes[j][i].successors)

    def test_should_create_intern_mesh_when_a_3_3_junction_is_created(self):
        simulator = Simulator()
        dictionary = {
            Orientation.NORTH: (3, 3),
            Orientation.EAST: (3, 3)
        }
        rp = RightPriorityJunction(simulator, dictionary)
        self.assertEquals({rp.nodes[0][1]}, set(rp.nodes[0][0].successors))
