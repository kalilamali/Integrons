#! /usr/bin/env python3
import os
import random
import numpy as np
from Bio import SeqIO

in_dir = 'mr0_test_cases'
out_dir = 'mr1_test_cases'
os.mkdir(out_dir)

files_list = os.listdir(in_dir)
files_list = [file for file in files_list if file.endswith('.fastq')]
for file in files_list:
    name = os.path.splitext(file)[0]
    old_file = os.path.join(in_dir, file)
    for r in SeqIO.parse(old_file, "fastq"):
        P = len(r.seq)
        I = 2
        indices = np.sort(np.random.randint(P, size = I))
        print(f'{r.id} size {P} split at {indices}')
        s1 = r[:indices[0]]
        s2 = r[indices[0]+1:indices[1]]
        s3 = r[indices[1]+1:]
        records = [s1, s2, s3]
        random.shuffle(records)
    new_file = os.path.join(out_dir, name)
    SeqIO.write(records, f"{new_file}.fastq", "fastq")
