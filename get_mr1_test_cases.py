#! /usr/bin/env python3
"""
get_mr1_test_cases.py
Creates fastq files with permutated reads from a folder containing fastq files.
Author      Loaiza, K.
Comments    Created: September, 2021.
"""

# Libraries
import os
import random
import numpy as np
from Bio import SeqIO

# Folders
in_dir = 'mr0_test_cases'
out_dir = 'mr1_test_cases'

# Create the new output folder
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
# Remove the old output folder
else:
    os.remove(out_dir)

# Get fastq files
files_list = os.listdir(in_dir)
files_list = [file for file in files_list if file.endswith('.fastq')]

for file in files_list:
    # Get filename without .fastq
    # In1538_MF974580.fastq > In1538_MF974580
    name = os.path.splitext(file)[0]
    # Get filepath
    # mr0_test_cases/In1538_MF974580.fastq
    old_file = os.path.join(in_dir, file)
    # Open the fastq file
    for r in SeqIO.parse(old_file, 'fastq'):
        # Get the lenght of the fastq sequence
        P = len(r.seq)
        # Get I random indices
        I = 2
        indices = np.sort(np.random.randint(P, size = I))
        print(f'{r.id} size {P} split at {indices}')
        # Get the chunks of sequences
        s1 = r[:indices[0]]
        s2 = r[indices[0]+1:indices[1]]
        s3 = r[indices[1]+1:]
        # Randomly shuffle the chunks of sequences
        records = [s1, s2, s3]
        random.shuffle(records)
    # Get the new filepath
    new_file = os.path.join(out_dir, name)
    # Save the chunks of sequences in one fastq file
    SeqIO.write(records, f'{new_file}.fastq', 'fastq')
