import os

# Stores the the root of the tests folder in the root_tests variable so it can be run on any machine.
root_tests = os.path.dirname(os.path.realpath(__file__))

def read_command_file_contents(file_name):
    with open(root_tests + file_name, 'r') as f:
        data = [x.strip('\n') for x in f.readlines()]
    return data