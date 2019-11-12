import numpy as np
import argparse
import matplotlib.pyplot as pyplot
from matplotlib import rc
from mpl_toolkits.mplot3d import Axes3D

class SystemSetup:
    def __init__(self, N_particles: int = 500, reduced_rho:
                 (int, float) = 0.9):
        """
        A function that sets up the system for the Monte Carlo
        simulation. 

        Parameters
        ----------
        N_particles : int
            the number of particles (default: 500)
        reduced_rho : float
            the reduced density (default: 0.9)
        """
        self.N_particles = N_particles
        self.reduced_rho = reduced_rho
        self.box_length = np.cbrt(self.N_particles / self.reduced_rho)
        self.coordinates = (0.5 - np.random.rand(self.N_particles, 3)) * \
                            self.box_length
    
    # SystemSetup: finished 


class MonteCarlo:
    def __init__(self, system: object = None, energy: object = None,
                 args: object = None):
        """
        A function that runs 

        """
    pass


def initialize():
    """
    An argument parser as an initializing function. 
    """
    parser = argparse.ArgumentParser(
        prog='mcfluid',
        description='This program performs a Monte Carlo simulation on \
        Lennard-Jones fluid')
    parser.add_argument('-N',
                        '--N_particles',
                        required=False,
                        type=int,
                        default=500,
                        help='The number of particles in the simulation \
                            box. Default: 500.')
    parser.add_argument('-T',
                        '--reduced_T',
                        required=False,
                        type=float,
                        default=0.9,
                        help='The reduced temperature ranging from 0 to 1. \
                            Default: 0.9.')
    parser.add_argument('-r',
                        '--reduced_rho',
                        required=False,
                        type=float,
                        default=0.9,
                        help='The reduced density of the particles ranging \
                            from 0 to 1. Default: 0.9.')
    parser.add_argument('-n',
                        '--n_steps',
                        required=False,
                        type=int,
                        default=1000000,
                        help='The number of Monte Carlo steps. Default: 1M.')
    parser.add_argument('-fe',
                        '--freq_ener',
                        required=False,
                        type=int,
                        default=1000,
                        help='The output frequency of energy as the stdout. \
                            Default: 1000.')
    parser.add_argument('-ft',
                        '--freq_traj',
                        required=False,
                        type=int,
                        default=100000,
                        help='The output frequency of the trajectory data. \
                            Default: 100000.')
    parser.add_argument('-m',
                        '--max_d',
                        required=False,
                        type=float,
                        default=0.1,
                        help='The initial maximum of the displacement. \
                            Default: 0.1.')
    parser.add_argument('-e',
                        '--energy',
                        required=False,
                        type=str,
                        choices=['LJ', 'Buckingham', 'UnitlessLJ'],
                        default='UnitlessLJ',
                        help='The energy function used to calculate the \
                            interactions between the particles in the fluid \
                            Default: "UnitLessLJ".')
    
    args_parse = parser.parse_args()

    return args_parse

def main():
    args = initialize()

