import numpy as np
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
        cls.parser = monte_carlo.initialize()
        np.random.seed()

    def test_system_init(self):
        """
        A function for the unit tests of the __init__ function in the class 
        SystemSetup
        """
        expected_coords = [-3.3169090299280337,
                           0.8789538182682277, -1.0191207180226685]
        self.assertEqual(self.sys_obj.N_particles, 500)
        self.assertEqual(self.sys_obj.reduced_rho, 0.9)
        self.assertEqual(self.sys_obj.box_length, 8.220706914434901)
        self.assertEqual(len(self.sys_obj.coordinates), 500)
        self.assertEqual(list(self.sys_obj.coordinates[0]), expected_coords)

    def test_MC_init(self):
        """
        A function for the unit tests of the __init__ function in the class 
        MonteCarlo
        """
        pass

    def test_MC_args(self):
        """
        A function for the unit tests of the argument parser of the class
        MonteCarlo (the funciton: initialize())
        """
        self.assertEqual(self.parser.N_particles, 500)
        self.assertEqual(self.parser.reduced_T, 0.9)
        self.assertEqual(self.parser.reduced_rho, 0.9)
        self.assertEqual(self.parser.n_steps, 1000000)
        self.assertEqual(self.parser.freq_ener, 1000)
        self.assertEqual(self.parser.freq_traj, 100000)
        self.assertEqual(self.parser.max_d, 0.1)
        self.assertEqual(self.parser.energy, 'UnitlessLJ')




if __name__ == '__main__':
    unittest.main()
