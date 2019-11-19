import energy
import unittest
import numpy as np


class TestEnergyModels(unittest.TestCase):
    def test_LennardJones(self):
        # create a model with default paramters
        model = energy.LennardJones()
        energy_2 = model.calc_energy(2)
        self.assertAlmostEqual(energy_2, -0.03076171875)
        self.assertEqual(model.cutoff_correction(), 0)

    def test_Buckingham(self):
        model = energy.Buckingham()
        energy_1 = model.calc_energy(1)
        self.assertAlmostEqual(energy_1, -0.63212055588)
        self.assertEqual(model.cutoff_correction(), 0)

    def test_UnitlessLennardJones(self):
        model = energy.UnitlessLennardJones()
        energy_1 = model.calc_energy(1)
        self.assertEqual(energy_1, 0)
        self.assertEqual(model.cutoff_correction(1, 1, 1), -5.585053606381854)

    def test_UnitlessLennardJones_factory(self):
        model = energy.Energy()
        coord = np.zeros((1, 3))
        energy_1 = model.calc_init_ener(coord, 1)
        self.assertEqual(energy_1, 0)

    def test_LennardJones_factory(self):
        model = energy.Energy('LJ')
        coord = np.array([[1, 2, 3], [0, 0, 0]])
        energy_1 = model.calc_init_ener(coord, 3)
        self.assertEqual(energy_1, -0.2187499999999999)


if __name__ == '__main__':
    unittest.main()
