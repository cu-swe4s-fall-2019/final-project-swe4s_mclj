# final-project-swe4s_mclj

## Continuous Integration Status
![](https://travis-ci.com/cu-swe4s-fall-2019/final-project-swe4s_mclj.svg?branch=master)

## Installation
To use this package, you need to have [Python3](https://www.python.org/download/releases/3.0/) in your environment. And the used packages are listed below.

### Used Packages
* os
* sys
* abc
* time
* numpy
* argparse
* unittest
* matplotlib
* pycodestyle

## Usage
Use `python monte_carlo.py` to conduct basic simulation. If you want to simulate different configuration, you can set the following arguments to `monte_carlo.py`:
1. `-N`: The number of particles in the simulation box. Default: 500.
2. `-T`: The reduced temperature ranging from 0 to 1. Default: 0.9.
3. `-r`: The reduced density of the particles ranging from 0 to 1. Default: 0.9.
4. `-n`: The number of Monte Carlo steps. Default: 1M.
5. `-fe`: The output frequency of energy as the stdout. Default: 1000.
6. `-ft`: The output frequency of the trajectory data. Default: 100000.
7. `-m`: The initial maximum of the displacement. Default: 0.1.
8. `-e`: The energy function used to calculate the interactions between the particles in the fluid Default: "UnitLessLJ".
9. `-p`: whether to plot the ouput the coordinates on updates
