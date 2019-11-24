import numpy as np
import argparse
import energy
import matplotlib.pyplot as plt
import sys
import os
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
        A initializing function for the class MonteCarlo

        Parameters
        ----------
        system : obj
            A SystemSetup object which initializes the Monte Carlo system
        energy : obj
            An Energy object which specifies the types of energy
        args : obj
            An arguement parser object returned by the function initialize
        """
        # get parameters from the class SystemSetup
        self.N_particles = system.N_particles
        self.coordinates = system.coordinates
        self.box_length = system.box_length

        # get parameters from the class Energy (need to check with CJ)
        self.init_ener = energy.calc_init_ener(
            self.coordinates, self.box_length)
        self.tail = energy.calc_tail(self.N_particles, self.box_length)
        self.energy = energy    # to extract the attributes in Energy class

        # get parameters from the method initialize
        self.args = args

    def metropolis_mc(self, delta_e: float, beta: float):
        """
        A function which implements the Metropolis-Hastings algorithm to decide
        whether to accept or reject the proposed moves.

        Parameters
        ----------
        delta_e : float
            The difference between the proposed and the current energies
        beta : float
            The inverse temperature

        Returns
        -------
        accept : bool
            Whether to accept (accept = True) or reject (accept = False) the
            moves
        """
        if delta_e < 0:
            accept = True
        else:
            p_acc = np.exp(-beta * delta_e)

            if np.random.rand() < p_acc:
                accept = True
            else:
                accept = False
        return accept

    def adjust_moves(self, max_d, n_accept, n_trials):
        """
        A function for adjusting the displacement to adjust the
        acceptance rate.
        A too large or a too small displacement would result in
        particle overlaps/low acceptance rate and inefficient
        sampling, respectively. Therefore, when the acceptance
        rate is too high, the max displacement should be adjusted
        to be higher and vice versa.

        Parameters
        ----------
        max_d : float
            The specified maximum displacement of the trial
        n_accept : int
            The current number of accepted trials when the function
            is initiated.
        n_trials : int
            The number of trials that have been performed when the function
            is initiated.

        Returns
        -------
        max_d : float
            The adjusted max displacement
        n_trials : int
            The updated number of total trials performed
        n_accept : int
            The updated number of accepted trials
        """
        acc_rate = float(n_accept) / float(n_trials)
        if acc_rate < 0.38:
            max_d *= 0.8
        elif acc_rate > 0.42:
            max_d *= 1.2

        n_trials, n_accept = 0, 0

        return max_d, n_accept, n_trials

    def MC_simulation(self):
        """
        This is the primary function that perform a Monte Carlo simulation
        """
        # set the initial total pair energy between particles in the system
        total_pair_energy = self.init_ener
        print(f'total pair initial: {total_pair_energy}')
        tail_correction = self.tail
        print(f'tail correction: {tail_correction}')

        # set up an array to store energy values
        energy_array = np.zeros(self.args.n_steps)

        # start the Monte Carlo iterations
        n_trials = 0
        n_accept = 0

        # check to make sure we write to an empty file
        with open(self.args.traj_file, "w") as fn:
            pass
        for i_step in range(self.args.n_steps):
            # print(f'Step{i_step}:')
            n_trials += 1
            i_particle = np.random.randint(self.N_particles)
            random_displacement = (
                2.0 * np.random.rand(3) - 1.0) * self.args.max_d
            # print(f'random displacement: {random_displacement}')
            current_energy = self.energy.calc_pair_ener(
                self.coordinates, self.box_length, i_particle)
            # print(f'current energy: {current_energy}')
            proposed_coordinates = self.coordinates.copy()
            proposed_coordinates[i_particle] += random_displacement
            proposed_coordinates -= self.box_length * \
                np.round(proposed_coordinates / self.box_length)
            proposed_energy = self.energy.calc_pair_ener(
                proposed_coordinates, self.box_length, i_particle)
            # print(f'i particle: {i_particle}')
            # print(f'proposd energy: {proposed_energy}')
            delta_e = proposed_energy - current_energy
            beta = 1.0 / self.args.reduced_T
            accept = self.metropolis_mc(delta_e, beta)
            # print(f'accept: {accept}')
            if accept:
                total_pair_energy += delta_e
                n_accept += 1
                self.coordinates[i_particle] += random_displacement
                self.coordinates -= self.box_length * \
                    np.round(self.coordinates / self.box_length)
            total_energy = (total_pair_energy +
                            tail_correction) / self.N_particles
            # print(f'total energy: {total_energy}')
            energy_array[i_step] = total_energy
            if np.mod(i_step + 1, self.args.freq_ener) == 0:
                print(i_step + 1, energy_array[i_step])
                # plot
                if args.plot:
                    ax = plt.axes(projection='3d')
                    ax.set_xlim([-self.box_length/2, self.box_length/2])
                    ax.set_ylim([-self.box_length/2, self.box_length/2])
                    ax.set_zlim([-self.box_length/2, self.box_length/2])
                    for i in range(self.args.N_particles):
                        ax.plot3D([self.coordinates[i, 0]],
                                  [self.coordinates[i, 1]],
                                  [self.coordinates[i, 2]], 'o')
                    plt.pause(0.05)
            # output traj
            with open(self.args.traj_file, "a+") as fn:
                # if prefer to output trajectories, open the output file
                if np.mod(i_step + 1, self.args.freq_traj) == 0:
                    fn.write(f'Step: {i_step + 1} \n')
                    for i_atom in range(len(self.coordinates)):
                        fn.write(
                            f'{self.coordinates[i_atom, 0]} \
                              {self.coordinates[i_atom, 1]} \
                              {self.coordinates[i_atom, 2]} \n')

            self.args.max_d, n_accept, n_trials = self.adjust_moves(
                self.args.max_d, n_accept, n_trials)

        self.energy_array = energy_array

        return True

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
    parser.add_argument('-p',
                        '--plot',
                        required=False,
                        type=bool,
                        default=True,
                        action='store_false',
                        help='whether to plot the ouput the \
                            coordinates on updates')

    args_parse = parser.parse_args()

    return args_parse


if __name__ == "__main__":
    args = initialize()
    new_system = SystemSetup(N_particles=args.N_particles,
                             reduced_rho=args.reduced_rho)
    energy = energy.Energy()
    args.traj_file = 'traj_output'
    sim = MonteCarlo(system=new_system, energy=energy, args=args)
    sim.MC_simulation()
    sys.exit(0)
