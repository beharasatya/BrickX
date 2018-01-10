from unittest import TestCase
from src.mars_rovers import MarsRover


class MarsRoverTest(TestCase):
    # def __init__(self):
    #     self.setUp()

    def setUp(self):
        self.bnd_x = 10
        self.bnd_y = 20
        self.rover1 = MarsRover(1, 2, 'N', self.bnd_x, self.bnd_y)
        self.rover2 = MarsRover(3, 3, 'E', self.bnd_x, self.bnd_y)

    def test_rover1_move(self):
        self.rover1.move('LMLMLMLMM')
        self.assertEqual(self.rover1.x, 1)
        self.assertEqual(self.rover1.y, 3)
        self.assertEqual(self.rover1.direction, 'N')

    def test_rover2_move(self):
        self.rover2.move('MMRMMRMRRM')
        self.assertEqual(self.rover2.x, 5)
        self.assertEqual(self.rover2.y, 1)
        self.assertEqual(self.rover2.direction, 'E')


