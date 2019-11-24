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

## Profiling and Improvement
**Command**: `python3 -m cProfile -s tottime monte_carlo.py -N 20 -n 100000`
```
65234309 function calls (61272000 primitive calls) in 81.529 seconds

Ordered by: internal time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
3800190   20.090    0.000   20.090    0.000 energy.py:92(calc_energy)
```
To speed up our simulation process, we utilized `cProfile` module to analyze the bottleneck of our program. Based on the profiling result, we want to speed up `calc_energy`. First, let's talk about `calc_energy`. This function takes a floating point `r` (radius) as input, and uses this parameter to calculate the corresponding energy. Thus, in order to improve the performance of `calc_energy`, we added a hash table such as a cache to store calculated energy of known `r`. As the result, the cache makes `calc_energy` around *1.449799197* times faster than original method.
```
69034583 function calls (65072274 primitive calls) in 74.539 seconds

Ordered by: internal time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
3800190   13.387    0.000   13.855    0.000 energy.py:92(calc_energy)
```

## Results
To verify the correctness of our simulation, we compared our result with [the benchmark provided by NIST](https://mmlapps.nist.gov/srs/LJ_PURE/mc.htm).
