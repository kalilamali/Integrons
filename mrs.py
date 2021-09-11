#!/usr/bin/env python3
"""
mrs.py
Author      Loaiza, K.
Comments    Created: September, 2021.
"""

# Libraries
import os
from subprocess import check_call  # command tool

# Functions
def get_dirs(in_dir):
    """
    Function that takes an input folder and returns a list of all the dirs
    inside
    """
    dir_list = os.listdir(in_dir)
    dir_list = [os.path.join(in_dir, dir) for dir in dir_list]
    dir_list = [dir for dir in dir_list if os.path.isdir(dir)]
    return dir_list

# Number of metamorphic relations
mrs = 3
for m in range(0, mrs):
    # Number of replicas
    replicas = 5
    for r in range(0, replicas):
        cmd = (f"python3 group_intfinder.py"
        f" --in_dir mr{m}_test_cases"
        f" --out_dir test_cases_results/mr{m}_{r}")
        #print(cmd)
        # Run cmd on the shell
        check_call(cmd, shell=True)

        # Get the path for the results of each metamorphic relation and replica
        mr_dir = os.path.join(f"test_cases_results/mr{m}_{r}", 'intfinder_results_0.5_0.5_0.5')
        dir_list = get_dirs(mr_dir)
        for dir in dir_list:
            seq_file = os.path.basename(dir)
            observed = ''
            expected = seq_file.split('_')[0] #In560_HE613853 -> In560
            # Open results file
            res_file = os.path.join(dir, 'results_tab.tsv')
            with open(res_file) as infile:
                for line in infile:
                    # Ignore headline
                    if line.startswith('Database'):
                        pass
                    else:
                        observed = line.split()[1]
            # Report
            if expected == observed:
                print(f'mr{m}\tpassed\t{seq_file}\t{observed}')
            if expected != observed:
                print(f'mr{m}\tfailed\t{seq_file}\t{observed}')
