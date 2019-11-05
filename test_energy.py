import energy
import unittest


class TestEnergyModels(unittest.TestCase):
    def testLennardJones(self):
        # create a model with default paramters
        model = energy.LennardJones()
        energy_2 = model.calc_energy(2)
        self.assertAlmostEqual(energy_2, -0.03076171875)
        self.assertEqual(model.cutoff_correction(), 0)

    def testBuckingham(self):
        model = energy.Buckingham()
        energy_1 = model.calc_energy(1)
        self.assertAlmostEqual(energy_1, -0.63212055588)
        self.assertEqual(model.cutoff_correction(), 0)

    def testUnitlessLennardJones(self):
        model = energy.UnitlessLennardJones()
        energy_1 = model.calc_energy(1)
        self.assertEqual(energy_1, 0)
        self.assertEqual(model.cutoff_correction(1, 1, 1), -5.585053606381854)


if __name__ == '__main__':
    unittest.main()