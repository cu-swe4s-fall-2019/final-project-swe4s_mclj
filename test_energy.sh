#!/bin/bash

test -e ssshtest || wget https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_style pycodestyle test_energy.py
assert_no_stdout
run test_style pycodestyle energy.py
assert_no_stdout

echo "...default constructor test..."
run test_default python3 energy.py
assert_exit_code 0
assert_stdout
