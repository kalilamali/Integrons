#!/usr/bin/env python3

"""
Validate.py
This program runs the validation for IntFinder.

Author      K.Loaiza
Comments    Created: Thursday, April 16, 2020
"""

import argparse
import os
import tempfile

from subprocess import check_call  # command tool

parser = argparse.ArgumentParser()
parser.add_argument('--in_dir', help='folder with input sequences')
parser.add_argument('--out_dir', help='folder to place the results')
parser.add_argument('--mutation_rate', default=0.01, help='mutation rate written as 0.01 for 1 percent')
parser.add_argument('--minimum_identity', default= 0.95, help='minimum identity threshold written as 0.95 for 95 percent')


def get_files(in_dir):
    """
    Function that takes an input folder and returns a list of all the fasta files inside
    """
    files_list = os.listdir(in_dir)
    files_list = [os.path.join(in_dir, file) for file in files_list if file.endswith('.fasta')]
    return files_list


def get_lenght(fasta):
    """
    Function that opens a fasta file (single line) and returns its lenght
    """
    with open(fasta, 'r') as infile:
        for line in infile:
            if line.startswith(">"):
                pass
            else:
                lenght = len(line)
    return lenght


def get_integer_percent(lenght, mutation_rate):
    """
    Function that takes a lenght and a mutation rate % and returns the % as an integer
    """
    integer_percent =  int(mutation_rate* lenght)
    return integer_percent


def get_msbar_cmd(fasta, integer_percent, mutation_rate, out_dir):
    """
    Function that takes a fasta and an integer percent and returns an msbar command
    """
    mutated_fasta_dir = os.path.join(out_dir, 'mutated_fastas' + '_' + str(mutation_rate))
    if not os.path.exists(mutated_fasta_dir):
        os.mkdir(mutated_fasta_dir)

    mutated_fasta = os.path.join(mutated_fasta_dir, os.path.basename(fasta))

    msbar_command = ("msbar"
    f" -sequence {fasta}"
    f" -count {integer_percent}"
    " -point 4"  # 4 : Changes
    " -block 0"  # 0 : None
    " -codon 0"  # 0 : None
    f" -outseq {mutated_fasta}")
    return msbar_command, mutated_fasta


def get_intfinder_cmd(mutated_fasta, mutation_rate, identity_value, out_dir):
    """
    Function that takes a mutated fasta and returns an intfinder command
    """
    intfinder_results_dir = os.path.join(out_dir, 'intfinder_results' + '_' + str(mutation_rate) + '_' + str(identity_value))
    if not os.path.exists(intfinder_results_dir):
        os.mkdir(intfinder_results_dir)

    intfinder_results_path = os.path.join(intfinder_results_dir, os.path.splitext(os.path.basename(mutated_fasta))[0])
    if not os.path.exists(intfinder_results_path):
        os.mkdir(intfinder_results_path)

    intfinder_command = ("python3 intfinder.py"
    f" -input_name1 {mutated_fasta}"
    f" -kma_path /Users/kalilamali/bin/kma"
    f" -output_name {intfinder_results_path}"
    f" -minimum_identity {identity_value}")
    return intfinder_command, intfinder_results_path


def get_integron_count(intfinder_results_path):
    """
    Function that a intfinder_results_path, finds a stats.out file and returns an integron_count
    """
    stats_file_path = intfinder_results_path + '_stats.out'

    integron_count = 0
    with open(stats_file_path) as infile:
        for line in infile:
            if line.startswith('In'):
                integron_count += 1
    return integron_count


if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.mkdir(args.out_dir)

    total_integron_count = 0

    files_list = get_files(args.in_dir)
    for fasta in files_list:
        lenght = get_lenght(fasta)
        integer_percent = get_integer_percent(lenght, args.mutation_rate)
        msbar_cmd, mutated_fasta = get_msbar_cmd(fasta, integer_percent, args.mutation_rate, args.out_dir)
        #print(msbar_cmd)
        check_call(msbar_cmd, shell=True)

        intfinder_cmd, intfinder_results_path = get_intfinder_cmd(mutated_fasta, args.mutation_rate, args.minimum_identity, args.out_dir)
        #print(intfinder_cmd)
        check_call(intfinder_cmd, shell=True)

        integron_count = get_integron_count(intfinder_results_path)
        total_integron_count += integron_count

    results_file = os.path.join(args.out_dir, 'validation_results.tsv')
    if os.path.exists(results_file) is False:
        with open(results_file, 'w') as outfile:
            print(f'mutation_rate\tidentity\tintegron_count', file=outfile)

    if os.path.exists(results_file):
        with open(results_file, 'a') as outfile:
            print(f'{args.mutation_rate}\t{args.minimum_identity}\t{total_integron_count}', file=outfile)
