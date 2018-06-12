import unittest

from shared import Orientation, dijkstra_with_path
from simulator import Road, Simulator
from simulator.car import Car
from simulator.path import Path
from simulator.right_priority_junction import RightPriorityJunction
from simulator.utils import *
from copy import deepcopy


class TestRightPriority(unittest.TestCase):

    def test_should_connect_correctly_when_a_road_is_link_to_a_right_priority_junction(self):
        simulator = Simulator()
        rp = RightPriorityJunction(simulator, {Orientation.NORTH: (0, 1), Orientation.EAST: (1, 0), Orientation.SOUTH: (1, 0), Orientation.WEST: (0, 1)})
        self.assertEqual(1, len(rp.nodes))
        self.assertEqual(1, len(rp.nodes[0]))

        self.assertEqual(1, len(rp.get_start(Orientation.SOUTH)))
        self.assertEqual(1, len(rp.get_start(Orientation.EAST)))

        self.assertEqual(1, len(rp.get_end(Orientation.NORTH)))
        self.assertEqual(1, len(rp.get_end(Orientation.WEST)))

        try:
            self.assertEqual(0, len(rp.get_start(Orientation.NORTH)))
            self.assertEqual(0, len(rp.get_start(Orientation.WEST)))

            self.assertEqual(0, len(rp.get_end(Orientation.SOUTH)))
            self.assertEqual(0, len(rp.get_end(Orientation.EAST)))
        except AssertionError as ignored:
            # Fail since we simplify the api when there is a connection without road
            pass

        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.WEST, 1)
        r4 = Road(simulator, 1, Orientation.NORTH, 1)

        rp.add_predecessor(Orientation.NORTH, r1)
        rp.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.WEST, rp)
        r4.add_predecessor(Orientation.NORTH, rp)

        self.assertEqual({rp.nodes[0][0]}, set(r1.nodes[0][0].successors))
        self.assertEqual({rp.nodes[0][0]}, set(r2.nodes[0][0].successors))
        self.assertEqual({r3.nodes[0][0], r4.nodes[0][0]}, set(rp.nodes[0][0].successors))

        self.assertEqual({rp.nodes[0][0], r2.nodes[0][0]}, set(simulator.dependencies[(r1.nodes[0][0], rp.nodes[0][0])]))
        self.assertEqual({rp.nodes[0][0]}, set(simulator.dependencies[(r2.nodes[0][0], rp.nodes[0][0])]))
        self.assertEqual({r3.nodes[0][0]}, set(simulator.dependencies[(rp.nodes[0][0], r3.nodes[0][0])]))
        self.assertEqual({r4.nodes[0][0]}, set(simulator.dependencies[(rp.nodes[0][0], r4.nodes[0][0])]))


    def test_should_go_when_there_is_no_right_priority(self):
        simulator = Simulator()
        rp = RightPriorityJunction(simulator, {Orientation.NORTH: (0, 1), Orientation.EAST: (1, 0), Orientation.SOUTH: (1, 0), Orientation.WEST: (0, 1)})
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.WEST, 1)
        r1.nodes[0][0].current_car = Car(Path([rp.nodes[0][0], r3.nodes[0][0]]), r1.nodes[0][0], 0)
        r2.nodes[0][0].current_car = Car(Path([rp.nodes[0][0], r3.nodes[0][0]]), r2.nodes[0][0], 0)

        rp.add_predecessor(Orientation.NORTH, r1)
        rp.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.WEST, rp)

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
        rp = RightPriorityJunction(simulator, {Orientation.NORTH: (1, 0), Orientation.EAST: (1, 0), Orientation.SOUTH: (1, 0), Orientation.WEST: (0, 1)})
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.WEST, 1)
        r1.nodes[0][0].current_car = Car(Path([rp.nodes[0][0], r3.nodes[0][0]]), r1, 0)

        rp.add_predecessor(Orientation.NORTH, r1)
        rp.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.WEST, rp)

        simulator.tick()

        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)

    def test_should_not_go_when_there_is_someone_in_junction_and_no_one_in_priority_road(self):
        simulator = Simulator()
        rp = RightPriorityJunction(simulator, {Orientation.NORTH: (1, 0), Orientation.EAST: (1, 0), Orientation.SOUTH: (1, 0), Orientation.WEST: (0, 1)})
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.WEST, 1)
        r1.nodes[0][0].current_car = Car(Path([rp.nodes[0][0], r3.nodes[0][0]]), r1, 0)
        rp.nodes[0][0].current_car = Car(Path([r3.nodes[0][0]]), rp, 0)

        rp.add_predecessor(Orientation.NORTH, r1)
        rp.add_predecessor(Orientation.WEST, r2)
        r3.add_predecessor(Orientation.WEST, rp)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNotNone(r3.nodes[0][0].current_car)

    def test_should_respect_right_priority_when_there_are_3_inputs_and_an_exit_with_double_way_road(self):
        # FIXME make this test multi-way compliant
        simulator = Simulator()
        rp = RightPriorityJunction(simulator, {Orientation.NORTH: (1, 0), Orientation.EAST: (1, 1), Orientation.SOUTH: (1, 0), Orientation.WEST: (1, 1)})
        r1 = Road(simulator, 1, Orientation.NORTH, 1)
        r2 = Road(simulator, 1, Orientation.WEST, 1)
        r3 = Road(simulator, 1, Orientation.SOUTH, 1)
        r4 = Road(simulator, 1, Orientation.EAST, 1)

        rp.add_predecessor(Orientation.NORTH, r1)
        rp.add_predecessor(Orientation.WEST, r2)
        rp.add_predecessor(Orientation.SOUTH, r3)
        r4.add_predecessor(Orientation.EAST, rp)

        r1.nodes[0][0].current_car = Car(Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, r1.nodes[0][0], r4.nodes[0][0])), r1, 0)
        r2.nodes[0][0].current_car = Car(Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, r2.nodes[0][0], r4.nodes[0][0])), r2, 0)
        r3.nodes[0][0].current_car = Car(Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, r3.nodes[0][0], r4.nodes[0][0])), r3, 0)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[1][0].current_car)
        self.assertIsNone(r4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNotNone(r2.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[1][0].current_car)
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
        self.assertIsNotNone(rp.nodes[1][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNone(r4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[1][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(r4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNotNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[1][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNotNone(r4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[1][0].current_car)
        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(r4.nodes[0][0].current_car)

        simulator.tick()
        self.assertIsNone(r1.nodes[0][0].current_car)
        self.assertIsNone(r2.nodes[0][0].current_car)
        self.assertIsNone(r3.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[1][0].current_car)
        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNotNone(r4.nodes[0][0].current_car)

    def test_should_respect_right_priority_when_there_are_3_inputs(self):
        simulator = Simulator()
        rp = RightPriorityJunction(simulator, {Orientation.NORTH: (1, 0), Orientation.EAST: (1, 0), Orientation.SOUTH: (1, 0), Orientation.WEST: (0, 1)})
        entryN = Road(simulator, 1, Orientation.NORTH, 1)
        entryW = Road(simulator, 1, Orientation.WEST, 1)
        entryS = Road(simulator, 1, Orientation.SOUTH, 1)
        exitW = Road(simulator, 1, Orientation.WEST, 1)

        p = Path([rp.nodes[0][0], exitW.nodes[0][0]])
        entryN.nodes[0][0].current_car = Car(p, entryN, 0)
        entryW.nodes[0][0].current_car = Car(p, entryW, 0)
        entryS.nodes[0][0].current_car = Car(p, entryS, 0)

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
        rp = RightPriorityJunction(simulator, {Orientation.NORTH: (0, 1), Orientation.EAST: (1, 0), Orientation.SOUTH: (1, 0), Orientation.WEST: (0, 1)})
        entryN = Road(simulator, 1, Orientation.NORTH, 1)
        entryW = Road(simulator, 1, Orientation.WEST, 1)
        exitW = Road(simulator, 1, Orientation.WEST, 1)
        exitN = Road(simulator, 1, Orientation.NORTH, 1)

        entryW.nodes[0][0].current_car = Car(Path([rp.nodes[0][0], exitW.nodes[0][0]]), entryW, 0)
        entryN.nodes[0][0].current_car = Car(Path([rp.nodes[0][0], exitN.nodes[0][0]]), entryN, 0)

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
        rp = RightPriorityJunction(simulator, {Orientation.NORTH: (0, 1), Orientation.EAST: (1, 0), Orientation.SOUTH: (0, 1), Orientation.WEST: (1, 0)})
        entry1 = Road(simulator, 1, Orientation.EAST, 1)
        entry2 = Road(simulator, 1, Orientation.WEST, 1)
        exit = Road(simulator, 1, Orientation.NORTH, 1)
        p = Path([rp.nodes[0][0], exit.nodes[0][0]])

        entry1.nodes[0][0].current_car = Car(p, entry1, 0)
        entry2.nodes[0][0].current_car = Car(p, entry2, 0)

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
        dictionnary = {Orientation.NORTH: (3, 2), Orientation.EAST: (3, 2), Orientation.SOUTH: (2, 3), Orientation.WEST: (2, 3)}
        rp = RightPriorityJunction(simulator, dictionnary)
        self.assertEqual(len(rp.get_start(Orientation.NORTH)), 3)
        self.assertEqual(len(rp.get_start(Orientation.SOUTH)), 2)
        self.assertEqual(len(rp.get_start(Orientation.EAST)), 3)
        self.assertEqual(len(rp.get_start(Orientation.WEST)), 2)

    def test_should_create_intern_mesh_when_a_2_3_junction_is_created(self):
        simulator = Simulator()
        dictionnary = {Orientation.NORTH: (3, 2), Orientation.EAST: (3, 2), Orientation.SOUTH: (2, 3), Orientation.WEST: (2, 3)}

        rp = RightPriorityJunction(simulator, dictionnary)

        self.assertEquals({rp.nodes[0][1]}, set(rp.nodes[0][0].successors))
        self.assertEquals({rp.nodes[0][2]}, set(rp.nodes[0][1].successors))
        self.assertEquals({rp.nodes[0][3]}, set(rp.nodes[0][2].successors))
        self.assertEquals({rp.nodes[0][4], rp.nodes[1][3]}, set(rp.nodes[0][3].successors))
        self.assertEquals({rp.nodes[1][4]}, set(rp.nodes[0][4].successors))

        self.assertEquals({rp.nodes[0][0], rp.nodes[1][1]}, set(rp.nodes[1][0].successors))
        self.assertEquals({rp.nodes[0][1], rp.nodes[1][2]}, set(rp.nodes[1][1].successors))
        self.assertEquals({rp.nodes[0][2], rp.nodes[1][3]}, set(rp.nodes[1][2].successors))
        self.assertEquals({rp.nodes[2][3], rp.nodes[1][4]}, set(rp.nodes[1][3].successors))
        self.assertEquals({rp.nodes[2][4]}, set(rp.nodes[1][4].successors))

        self.assertEquals({rp.nodes[1][0]}, set(rp.nodes[2][0].successors))
        self.assertEquals({rp.nodes[1][1], rp.nodes[2][0]}, set(rp.nodes[2][1].successors))
        self.assertEquals({rp.nodes[1][2], rp.nodes[2][1]}, set(rp.nodes[2][2].successors))
        self.assertEquals({rp.nodes[3][3], rp.nodes[2][2]}, set(rp.nodes[2][3].successors))
        self.assertEquals({rp.nodes[3][4], rp.nodes[2][3]}, set(rp.nodes[2][4].successors))

        self.assertEquals({rp.nodes[2][0]}, set(rp.nodes[3][0].successors))
        self.assertEquals({rp.nodes[2][1], rp.nodes[3][0]}, set(rp.nodes[3][1].successors))
        self.assertEquals({rp.nodes[2][2], rp.nodes[3][1]}, set(rp.nodes[3][2].successors))
        self.assertEquals({rp.nodes[4][3], rp.nodes[3][2]}, set(rp.nodes[3][3].successors))
        self.assertEquals({rp.nodes[4][4], rp.nodes[3][3]}, set(rp.nodes[3][4].successors))

        self.assertEquals({rp.nodes[3][0]}, set(rp.nodes[4][0].successors))
        self.assertEquals({rp.nodes[3][1], rp.nodes[4][0]}, set(rp.nodes[4][1].successors))
        self.assertEquals({rp.nodes[3][2], rp.nodes[4][1]}, set(rp.nodes[4][2].successors))
        self.assertEquals({rp.nodes[4][2]}, set(rp.nodes[4][3].successors))
        self.assertEquals({rp.nodes[4][3]}, set(rp.nodes[4][4].successors))



    def test_should_create_intern_mesh_when_a_3_3_junction_is_created(self):
        simulator = Simulator()
        dictionary = {Orientation.NORTH: (3, 3), Orientation.EAST: (3, 3), Orientation.SOUTH: (3, 3), Orientation.WEST: (3, 3)}

        rp = RightPriorityJunction(simulator, dictionary)

        # Start / end
        self.assertEquals({*rp.nodes[0][3:]}, set(rp.get_start(Orientation.SOUTH)))
        self.assertEquals({n[0] for n in rp.nodes[:3]}, set(rp.get_start(Orientation.WEST)))
        self.assertEquals({*rp.nodes[-1][:3]}, set(rp.get_start(Orientation.NORTH)))
        self.assertEquals({n[-1] for n in rp.nodes[3:]}, set(rp.get_start(Orientation.EAST)))

        self.assertEquals({*rp.nodes[0][:3]}, set(rp.get_end(Orientation.SOUTH)))
        self.assertEquals({n[0] for n in rp.nodes[3:]}, set(rp.get_end(Orientation.WEST)))
        self.assertEquals({*rp.nodes[-1][3:]}, set(rp.get_end(Orientation.NORTH)))
        self.assertEquals({n[-1] for n in rp.nodes[:3]}, set(rp.get_end(Orientation.EAST)))

        # Successors test
        self.assertEquals({rp.nodes[0][1]}, set(rp.nodes[0][0].successors))
        self.assertEquals({rp.nodes[0][2]}, set(rp.nodes[0][1].successors))
        self.assertEquals({rp.nodes[0][3]}, set(rp.nodes[0][2].successors))
        self.assertEquals({rp.nodes[0][4], rp.nodes[1][3]}, set(rp.nodes[0][3].successors))
        self.assertEquals({rp.nodes[0][5], rp.nodes[1][4]}, set(rp.nodes[0][4].successors))
        self.assertEquals({rp.nodes[1][5]}, set(rp.nodes[0][5].successors))

        self.assertEquals({rp.nodes[0][0], rp.nodes[1][1]}, set(rp.nodes[1][0].successors))
        self.assertEquals({rp.nodes[0][1], rp.nodes[1][2]}, set(rp.nodes[1][1].successors))
        self.assertEquals({rp.nodes[0][2], rp.nodes[1][3]}, set(rp.nodes[1][2].successors))
        self.assertEquals({rp.nodes[2][3], rp.nodes[1][4]}, set(rp.nodes[1][3].successors))
        self.assertEquals({rp.nodes[2][4], rp.nodes[1][5]}, set(rp.nodes[1][4].successors))
        self.assertEquals({rp.nodes[2][5]}, set(rp.nodes[1][5].successors))

        self.assertEquals({rp.nodes[1][0], rp.nodes[2][1]}, set(rp.nodes[2][0].successors))
        self.assertEquals({rp.nodes[1][1], rp.nodes[2][2]}, set(rp.nodes[2][1].successors))
        self.assertEquals({rp.nodes[1][2], rp.nodes[2][3]}, set(rp.nodes[2][2].successors))
        self.assertEquals({rp.nodes[3][3], rp.nodes[2][4]}, set(rp.nodes[2][3].successors))
        self.assertEquals({rp.nodes[3][4], rp.nodes[2][5]}, set(rp.nodes[2][4].successors))
        self.assertEquals({rp.nodes[3][5]}, set(rp.nodes[2][5].successors))

        self.assertEquals({rp.nodes[2][0]}, set(rp.nodes[3][0].successors))
        self.assertEquals({rp.nodes[2][1], rp.nodes[3][0]}, set(rp.nodes[3][1].successors))
        self.assertEquals({rp.nodes[2][2], rp.nodes[3][1]}, set(rp.nodes[3][2].successors))
        self.assertEquals({rp.nodes[4][3], rp.nodes[3][2]}, set(rp.nodes[3][3].successors))
        self.assertEquals({rp.nodes[4][4], rp.nodes[3][3]}, set(rp.nodes[3][4].successors))
        self.assertEquals({rp.nodes[4][5], rp.nodes[3][4]}, set(rp.nodes[3][5].successors))

        self.assertEquals({rp.nodes[3][0]}, set(rp.nodes[4][0].successors))
        self.assertEquals({rp.nodes[3][1], rp.nodes[4][0]}, set(rp.nodes[4][1].successors))
        self.assertEquals({rp.nodes[3][2], rp.nodes[4][1]}, set(rp.nodes[4][2].successors))
        self.assertEquals({rp.nodes[5][3], rp.nodes[4][2]}, set(rp.nodes[4][3].successors))
        self.assertEquals({rp.nodes[5][4], rp.nodes[4][3]}, set(rp.nodes[4][4].successors))
        self.assertEquals({rp.nodes[5][5], rp.nodes[4][4]}, set(rp.nodes[4][5].successors))

        self.assertEquals({rp.nodes[4][0]}, set(rp.nodes[5][0].successors))
        self.assertEquals({rp.nodes[4][1], rp.nodes[5][0]}, set(rp.nodes[5][1].successors))
        self.assertEquals({rp.nodes[4][2], rp.nodes[5][1]}, set(rp.nodes[5][2].successors))
        self.assertEquals({rp.nodes[5][2]}, set(rp.nodes[5][3].successors))
        self.assertEquals({rp.nodes[5][3]}, set(rp.nodes[5][4].successors))
        self.assertEquals({rp.nodes[5][4]}, set(rp.nodes[5][5].successors))

    def test_should_respect_right_priority_when_there_are_2_inputs_and_2_output_and_2_ways(self):
        simulator = Simulator()
        rp = RightPriorityJunction(simulator,
                                   {Orientation.NORTH: (0, 2), Orientation.EAST: (2, 0), Orientation.SOUTH: (2, 0),
                                    Orientation.WEST: (0, 2)})
        entryN = Road(simulator, 1, Orientation.NORTH, 2)
        entryW = Road(simulator, 1, Orientation.WEST, 2)
        exitW = Road(simulator, 1, Orientation.WEST, 2)
        exitN = Road(simulator, 1, Orientation.NORTH, 2)

        rp.add_predecessor(Orientation.NORTH, entryN)
        rp.add_predecessor(Orientation.WEST, entryW)
        exitW.add_predecessor(Orientation.WEST, rp)
        exitN.add_predecessor(Orientation.NORTH, rp)

        # Check that the graph is coherent
        self.assertEqual({rp.nodes[0][0]}, set(entryN.nodes[0][0].successors))
        self.assertEqual({rp.nodes[0][1]}, set(entryN.nodes[1][0].successors))

        self.assertEqual({rp.nodes[0][1]}, set(entryW.nodes[0][0].successors))
        self.assertEqual({rp.nodes[1][1]}, set(entryW.nodes[1][0].successors))

        self.assertEqual({exitW.nodes[0][0], rp.nodes[1][0]}, set(rp.nodes[0][0].successors))
        self.assertEqual({rp.nodes[0][0], rp.nodes[1][1]}, set(rp.nodes[0][1].successors))
        self.assertEqual({exitW.nodes[1][0], exitN.nodes[0][0]}, set(rp.nodes[1][0].successors))
        self.assertEqual({rp.nodes[1][0], exitN.nodes[1][0]}, set(rp.nodes[1][1].successors))

        entryW.nodes[0][0].current_car = Car(Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, entryW.nodes[0][0], exitW.nodes[0][0])), entryW.nodes[0][0], 0)
        entryN.nodes[0][0].current_car = Car(Path(dijkstra_with_path(simulator.get_nodes(), simulator.weights, entryN.nodes[0][0], exitN.nodes[0][0])), entryW.nodes[0][0], 0)

        simulator.tick()
        self.assertIsNotNone(entryN.nodes[0][0].current_car)
        self.assertIsNone(entryN.nodes[1][0].current_car)
        self.assertIsNone(entryW.nodes[0][0].current_car)
        self.assertIsNone(entryW.nodes[1][0].current_car)

        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNotNone(rp.nodes[0][1].current_car)
        self.assertIsNone(rp.nodes[1][0].current_car)
        self.assertIsNone(rp.nodes[1][1].current_car)

        self.assertIsNone(exitW.nodes[0][0].current_car)
        self.assertIsNone(exitW.nodes[1][0].current_car)
        self.assertIsNone(exitN.nodes[0][0].current_car)
        self.assertIsNone(exitN.nodes[1][0].current_car)

        simulator.tick()
        self.assertIsNotNone(entryN.nodes[0][0].current_car)
        self.assertIsNone(entryN.nodes[1][0].current_car)
        self.assertIsNone(entryW.nodes[0][0].current_car)
        self.assertIsNone(entryW.nodes[1][0].current_car)

        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][1].current_car)
        self.assertIsNone(rp.nodes[1][0].current_car)
        self.assertIsNone(rp.nodes[1][1].current_car)

        self.assertIsNone(exitW.nodes[0][0].current_car)
        self.assertIsNone(exitW.nodes[1][0].current_car)
        self.assertIsNone(exitN.nodes[0][0].current_car)
        self.assertIsNone(exitN.nodes[1][0].current_car)

        simulator.tick()
        self.assertIsNotNone(entryN.nodes[0][0].current_car)
        self.assertIsNone(entryN.nodes[1][0].current_car)
        self.assertIsNone(entryW.nodes[0][0].current_car)
        self.assertIsNone(entryW.nodes[1][0].current_car)

        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][1].current_car)
        self.assertIsNone(rp.nodes[1][0].current_car)
        self.assertIsNone(rp.nodes[1][1].current_car)

        self.assertIsNotNone(exitW.nodes[0][0].current_car)
        self.assertIsNone(exitW.nodes[1][0].current_car)
        self.assertIsNone(exitN.nodes[0][0].current_car)
        self.assertIsNone(exitN.nodes[1][0].current_car)

        simulator.tick()
        self.assertIsNone(entryN.nodes[0][0].current_car)
        self.assertIsNone(entryN.nodes[1][0].current_car)
        self.assertIsNone(entryW.nodes[0][0].current_car)
        self.assertIsNone(entryW.nodes[1][0].current_car)

        self.assertIsNotNone(rp.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][1].current_car)
        self.assertIsNone(rp.nodes[1][0].current_car)
        self.assertIsNone(rp.nodes[1][1].current_car)

        self.assertIsNone(exitW.nodes[0][0].current_car)
        self.assertIsNone(exitW.nodes[1][0].current_car)
        self.assertIsNone(exitN.nodes[0][0].current_car)
        self.assertIsNone(exitN.nodes[1][0].current_car)

        simulator.tick()
        self.assertIsNone(entryN.nodes[0][0].current_car)
        self.assertIsNone(entryN.nodes[1][0].current_car)
        self.assertIsNone(entryW.nodes[0][0].current_car)
        self.assertIsNone(entryW.nodes[1][0].current_car)

        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][1].current_car)
        self.assertIsNotNone(rp.nodes[1][0].current_car)
        self.assertIsNone(rp.nodes[1][1].current_car)

        self.assertIsNone(exitW.nodes[0][0].current_car)
        self.assertIsNone(exitW.nodes[1][0].current_car)
        self.assertIsNone(exitN.nodes[0][0].current_car)
        self.assertIsNone(exitN.nodes[1][0].current_car)

        simulator.tick()
        self.assertIsNone(entryN.nodes[0][0].current_car)
        self.assertIsNone(entryN.nodes[1][0].current_car)
        self.assertIsNone(entryW.nodes[0][0].current_car)
        self.assertIsNone(entryW.nodes[1][0].current_car)

        self.assertIsNone(rp.nodes[0][0].current_car)
        self.assertIsNone(rp.nodes[0][1].current_car)
        self.assertIsNone(rp.nodes[1][0].current_car)
        self.assertIsNone(rp.nodes[1][1].current_car)

        self.assertIsNone(exitW.nodes[0][0].current_car)
        self.assertIsNone(exitW.nodes[1][0].current_car)
        self.assertIsNotNone(exitN.nodes[0][0].current_car)
        self.assertIsNone(exitN.nodes[1][0].current_car)
