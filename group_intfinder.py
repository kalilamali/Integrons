#!/usr/bin/env python3

"""Group_intfinder.py
This program runs intfinder for a folder containing many fastq files.

Author      K.Loaiza
Comments    Created: Thursday, April 18, 2020"""

import argparse
import os
import tempfile

from subprocess import check_call  # command tool

parser = argparse.ArgumentParser()
parser.add_argument('--in_dir', help='folder with input sequences')
parser.add_argument('--out_dir', help='folder to place the results')


def get_files(in_dir):
    """Function that takes an input folder and returns a list of all the fasta
    files inside"""
    files_list = os.listdir(in_dir)
    files_list = [os.path.join(in_dir, file) for file in files_list if file.endswith('.fastq')]
    return files_list


def get_intfinder_cmd(fasta, out_dir):
    """Function that takes a fasta and returns an intfinder command"""
    identity_value = 0.5
    coverage_value = 0.5
    depth_value = 0.5
    intfinder_results_dir = os.path.join(out_dir, f'intfinder_results_{coverage_value}_{identity_value}_{depth_value}')
    if not os.path.exists(intfinder_results_dir):
        os.mkdir(intfinder_results_dir)

    intfinder_results_path = os.path.join(intfinder_results_dir, os.path.splitext(os.path.basename(fasta))[0])
    if not os.path.exists(intfinder_results_path):
        os.mkdir(intfinder_results_path)

    intfinder_command = ("python3 intfinder/intfinder.py"
    f" -i {fasta}"
    f" -o {intfinder_results_path}"
    #f" -tmp {tmp_dir}"
    f" -mp /usr/bin/kma"
    f" -p /home/david/MyUnixWorkplace/intfinder_db"
    f" -l {coverage_value}"
    f" -t {identity_value}"
    f" -d {depth_value}"
    f" -x"
    f" -q ")

    return intfinder_command, intfinder_results_path


if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    files_list = get_files(args.in_dir)
    for fasta in files_list:
        intfinder_cmd, intfinder_results_path = get_intfinder_cmd(fasta, args.out_dir)
        #print(intfinder_cmd)
        check_call(intfinder_cmd, shell=True)
