#!/usr/bin/env python3
import os
from subprocess import check_call  # command tool

def get_dirs(in_dir):
    """
    Function that takes an input folder and returns a list of all the dirs inside
    """
    dir_list = os.listdir(in_dir)
    dir_list = [os.path.join(in_dir, dir) for dir in dir_list]
    dir_list = [dir for dir in dir_list if os.path.isdir(dir)]
    return dir_list

mrs = 3
for m in range(0, mrs):
    replicas = 5
    for r in range(0, replicas):
        cmd = f"python3 group_intfinder.py --in_dir mr{m}_test_cases --out_dir test_cases_results/mr{m}_{r}"
        #print(cmd)
        check_call(cmd, shell=True)

        mr_dir = os.path.join(f"test_cases_results/mr{m}_{r}", 'intfinder_results_0.5_0.5_0.5')

        dir_list = get_dirs(mr_dir)
        for dir in dir_list:
            seq_file = os.path.basename(dir)
            observed = ''
            expected = seq_file.split('_')[0] #In560_HE613853 -> In560
            res_file = os.path.join(dir, 'results_tab.tsv')
            with open(res_file) as infile:
                for line in infile:
                    if line.startswith('Database'):
                        pass
                    else:
                        observed = line.split()[1]
            if expected == observed:
                print(f'mr{m}\tpassed\t{seq_file}\t{observed}')
            if expected != observed:
                print(f'mr{m}\tfailed\t{seq_file}\t{observed}')
