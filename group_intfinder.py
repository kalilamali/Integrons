#!/usr/bin/env python3
"""
group_intfinder.py
Runs intfinder for a folder containing fastq files.
Author      Loaiza, K.
Comments    Created: April, 2020.
"""

# Libraries
import os
import argparse
import tempfile
from subprocess import check_call  # command tool

# Menu
parser = argparse.ArgumentParser()
parser.add_argument('--in_dir', help='folder with input sequences')
parser.add_argument('--out_dir', help='folder to place the results')

# Functions
def get_files(in_dir):
    """
    Function that takes an input folder and returns a list of all the fastq
    files inside
    """
    # Get fastq files
    files_list = os.listdir(in_dir)
    files_list = [os.path.join(in_dir, file)
    for file
    in files_list
    if file.endswith('.fastq')]
    return files_list

def get_intfinder_cmd(fastq, out_dir):
    """
    Function that takes a fastq and returns an intfinder command
    """
    # Values range 0-1
    # For example 0.5 means 50% identity
    identity = 0.5
    coverage = 0.5
    depth = 0.5

    # New folder name with the values used
    # intfinder_results_0.5_0.5_0.5
    dir = f'intfinder_results_{coverage}_{identity}_{depth}'
    results_dir = os.path.join(out_dir, dir)
    # Create the new sub folder
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)

    # Get the filename to use it as a dirname
    # In431_AY029772.fastq > In431_AY029772
    dir = os.path.splitext(os.path.basename(fastq))[0]
    results_sub_dir = os.path.join(results_dir, dir)
    # Create the new sub sub folder
    if not os.path.exists(results_sub_dir):
        os.mkdir(results_sub_dir)

    # Get intfinder_db location
    db_loc = os.path.join(os.getcwd(), 'intfinder_db')

    # Create the intfinder command
    intfinder_cmd = ("python3 intfinder/intfinder.py"
    f" -i {fastq}"
    f" -o {results_sub_dir}"
    #f" -tmp {tmp_dir}"
    f" -mp /usr/bin/kma"
    f" -p {db_loc}"
    f" -l {coverage}"
    f" -t {identity}"
    f" -d {depth}"
    f" -x"
    f" -q ")
    return intfinder_cmd, results_sub_dir

# Main program
if __name__ == '__main__':
    # Menu
    args = parser.parse_args()

    # Create the new output folder
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    # Get fastq files
    files_list = get_files(args.in_dir)
    # For each file get an intfinder command
    for fastq in files_list:
        intfinder_cmd, results_sub_dir = get_intfinder_cmd(fastq, args.out_dir)
        #print(intfinder_cmd)
        # Run the intfinder command on the shell
        check_call(intfinder_cmd, shell=True)
