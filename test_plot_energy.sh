#!/bin/bash

test -e ssshtest || wget https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_style pycodestyle plot_energy.py
assert_no_stdout

run test_plot python3 python3 plot_energy.py -i results/result.txt -o test.png
assert_no_stdout
assert_exit_code
rm test.png