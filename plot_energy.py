import matplotlib.pyplot as plt
from matplotlib import rc
import argparse


def initialize():
    """
    An argument parser as an intializing function
    """

    parser = argparse.ArgumentParser(
        description='This code generate a plot of energy as a function of \
                    Monte Carlo steps given the input data file.')
    parser.add_argument('-i',
                        '--input',
                        type=str,
                        required=True,
                        help='The file name of the input data file.')
    parser.add_argument('-o',
                        '--output',
                        type=str,
                        required=True,
                        help='The file name of the output figure.')

    args_parse = parser.parse_args()
    return args_parse


def main():
    args = initialize()

    f = open(args.input, 'r')
    lines = f.readlines()
    f.close()

    n = 0     # line number
    step, energy = [], []
    meta_end = False   # if the part of metadata ends
    for l in lines:
        n += 1
        if meta_end is True:
            step.append(float(l.split()[0]))
            energy.append(float(l.split()[1]))
        if "tail correction" in l:
            meta_end = True

    print('Energy averaged over the last 100000 steps: %s' %
          str(sum(energy[-100:]) / len(energy[-100:])))

    rc('font', **{
        'family': 'sans-serif',
        'sans-serif': ['DejaVu Sans'],
        'size': 10
    })
    # Set the font used for MathJax - more on this later
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='serif')

    plt.figure()
    plt.plot(step[50:], energy[50:])
    plt.title('Total potential energy as a funtion of Monte Carlo steps')
    plt.xlabel('Monte Carlo step')
    plt.ylabel('Reduced potential energy')
    plt.grid()
    plt.savefig('results/' + args.output)


if __name__ == "__main__":
    main()
