#! /usr/bin/env python3
"""
get_mr0_test_cases.py
Creates fastq files with dummy scores from a folder containing fasta files.
Author      Loaiza, K.
Comments    Created: September, 2021.
"""

# Libraries
import os
from Bio import SeqIO

# Folders
in_dir = 'validation_seqs'
out_dir = 'mr0_test_cases'

# Create the new output folder
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
# Remove the old output folder
else:
    os.remove(out_dir)

# Get fasta files
files_list = os.listdir(in_dir)
files_list = [file for file in files_list if file.endswith('.fasta')]

for file in files_list:
    # Get filename without .fasta
    # In1538_MF974580.fasta > In1538_MF974580
    name = os.path.splitext(file)[0]
    # Get filepath
    # validation_seqs/In1538_MF974580.fasta
    old_file = os.path.join(in_dir, file)
    # Open the fasta file
    for r in SeqIO.parse(old_file, 'fasta'):
        # Assign dummy quality scores
        r.letter_annotations['solexa_quality'] = [40] * len(r)
    # Get the new filepath
    new_file = os.path.join(out_dir, name)
    # Save the fasta with quality scores (fastq)
    SeqIO.write(r, f'{new_file}.fastq', 'fastq')
