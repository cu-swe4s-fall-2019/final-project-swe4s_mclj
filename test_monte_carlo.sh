#!/bin/bash

test -e ssshtest || wget https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_style pycodestyle test_monte_carlo.py
assert_no_stdout
run test_style pycodestyle monte_carlo.py
assert_no_stdout

echo "...few particles..."
run test_few_particles python3 monte_carlo.py --N_particles 10 --n_steps 10000 --traj_file test.xyz
assert_stdout
assert_exit_code 0
rm test.xyz
