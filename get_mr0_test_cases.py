#! /usr/bin/env python3
import os
from Bio import SeqIO

in_dir = 'validation_seqs'
out_dir = 'mr0_test_cases'
os.mkdir(out_dir)

files_list = os.listdir(in_dir)
files_list = [file for file in files_list if file.endswith('.fasta')]
for file in files_list:
    name = os.path.splitext(file)[0]
    old_file = os.path.join(in_dir, file)
    for r in SeqIO.parse(old_file, "fasta"):
        r.letter_annotations["solexa_quality"] = [40] * len(r)
    new_file = os.path.join(out_dir, name)
    SeqIO.write(r, f"{new_file}.fastq", "fastq")
