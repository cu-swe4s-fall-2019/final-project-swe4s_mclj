import numpy as np
from abc import ABC, abstractmethod


class EnergyModel(ABC):
    """This class is an abstract class for all the energy functions that are
    going to be written. All energy functions that inherit this structure MUST
    have a calc_energy method and a cutoff_correction method.
    """

    @abstractmethod
    def calc_energy(self):
        pass

    @abstractmethod
    def cutoff_correction(self):
        pass


class LennardJones(EnergyModel):
    """Setup for the Lennard-Jones potential.
    Parameters
    ----------
    epsilon: float, int
    sigma: float, int
    """

    def __init__(self, epsilon: (int, float) = 0.5,
                 sigma: (int, float) = 1.0):
        try:
            self.sigma = float(sigma)
            self.epsilon = float(epsilon)
        except ValueError:
            print('Invalid input parameters, use default instead')
            self.sigma = 1.0
            self.epsilon = 0.5

    def calc_energy(self, r):
        return (4 * self.epsilon * ((self.sigma / r) ** 12
                                    - (self.sigma / r) ** 6))

    def cutoff_correction(self, cutoff=None, number_particles=None, box_length=None):
        return(0)


class Buckingham(EnergyModel):
    """Set-up for the Buckingham potential.

    Parameters
    ----------
    rho: float, int
    a: float, int
    c: float, int
    """

    def __init__(self, rho: (int, float) = 1.0, a: (int, float) = 1.0,
                 c: (int, float) = 1.0):
        self.rho = float(rho)
        self.a = float(a)
        self.c = float(c)

    def calc_energy(self, r):
        return self.a * np.exp(-r / self.rho) - self.c / r ** 6

    def cutoff_correction(self, cutoff=None, number_particles=None, box_length=None):
        return(0)

class UnitlessLennardJones(EnergyModel):
    """Set-up for the Buckingham potential.
    
    Parameters
    ----------
    r: float, int
    """

    def __init__(self):
        pass

    def calc_energy(self, r: (int, float) = None):
        return 4.0 * (np.power(1 / r, 12)
                      - np.power(1 / r, 6))

    def cutoff_correction(self, cutoff, number_particles, box_length):
        volume = np.power(box_length, 3)
        sig_by_cutoff3 = np.power(1.0 / cutoff, 3)
        sig_by_cutoff9 = np.power(sig_by_cutoff3, 3)
        e_correction = sig_by_cutoff9 - 3.0 * sig_by_cutoff3

        e_correction *= 8.0 / 9.0 * np.pi * number_particles / volume * number_particles

        return e_correction
