import numpy as np
import energy
import unittest
import monte_carlo


class TestMonteCarlo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        A function for instantiating SystemSetup class
        """
        np.random.seed(2019)
        # So the 1 st row of the first random number array, random.rand(500, 3)
        # will be [0.90348221, 0.39308051, 0.62396996]
        # Accordingly, the first row of
        # coordinates = (0.5 - np.random.rand(500, 3)) * box_length
        # should be [-3.31690899,  0.87895379, -1.01912071]
        cls.sys_obj = monte_carlo.SystemSetup()
        cls.energy = energy.Energy()
        cls.parser = monte_carlo.initialize()
        cls.sim = monte_carlo.MonteCarlo(
            cls.sys_obj, cls.energy, cls.parser)
        np.random.seed()

    def test_system_init(self):
        """
        A function for the unit tests of the
        __init__ function in the class SystemSetup
        """
        expected_coords = [-3.3169090299280337,
                           0.8789538182682277, -1.0191207180226685]
        self.assertEqual(self.sys_obj.N_particles, 500)
        self.assertEqual(self.sys_obj.reduced_rho, 0.9)
        self.assertEqual(self.sys_obj.box_length, 8.220706914434901)
        self.assertEqual(len(self.sys_obj.coordinates), 500)
        self.assertEqual(list(self.sys_obj.coordinates[0]), expected_coords)

    def test_args(self):
        """
        A function for the unit tests of the argument parser of the class
        MonteCarlo (the funciton: initialize())
        """
        self.assertEqual(self.parser.N_particles, 500)
        self.assertEqual(self.parser.reduced_T, 0.9)
        self.assertEqual(self.parser.reduced_rho, 0.9)
        self.assertEqual(self.parser.n_steps, 1000000)
        self.assertEqual(self.parser.freq_ener, 1000)
        self.assertEqual(self.parser.freq_traj, 1000)
        self.assertEqual(self.parser.max_d, 0.1)
        self.assertEqual(self.parser.energy, 'UnitlessLJ')

    def test_metropolis_mc(self):
        a = self.sim.metropolis_mc(-1, 0)
        self.assertTrue(a)
        b = self.sim.metropolis_mc(10, 1)
        self.assertFalse(b)

    def test_adjust_moves(self):
        a, b, c = self.sim.adjust_moves(10, 10, 10)
        self.assertEqual(a, 12.0)
        self.assertEqual(b, 0)
        self.assertEqual(c, 0)

    def test_MC_simulation(self):
        self.assertTrue(self.sim.MC_simulation)


if __name__ == '__main__':
    unittest.main()
