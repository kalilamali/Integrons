# IntFinder development and validation

This repository contains the scripts necessary to reproduce the validation of IntFinder (version 1.0).

1. Download this repository.
```
git clone https://github.com/kalilamali/integrons
```
2. Download IntFinder.
```
git clone https://bitbucket.org/genomicepidemiology/intfinder.git
```
3. Download IntFinder database.
```
git clone https://bitbucket.org/genomicepidemiology/intfinder_db.git
cd intfinder_db
python3 INSTALL.py
1
cd ..
```
4. Download KMA.
```
git clone https://bitbucket.org/genomicepidemiology/kma.git
cd kma && make
mv kma /usr/bin/
cd ..
```
5. Your folders and scripts should look like this:
```
/Integrons
  /intfinder
  /intfinder_db
  /kma
  /validation_seqs
  CITATION.cff
  get_mr0_test_cases.py
  get_mr1_test_cases.py
  get_mr2_test_cases.py
  group_intfinder.py
  mrs.py
  README.md
```
6. Create the test cases according to the metamorphic relations (MRs).
```
python3 get_mr0_test_cases.py
python3 get_mr1_test_cases.py
python3 get_mr2_test_cases.py
```
7. Run IntFinder for each test case.
```
python3 mrs.py
python3 mrs.py > report.tsv
```
# FAQ:

group_intfinder.py uses kma's location:\
/usr/bin/kma\
if kma is not in that location please update the script.

If you get:\
ModuleNotFoundError: No module named 'tabulate'\
ModuleNotFoundError: No module named 'cgecore'\
It can be fixed with the following comands:
```
pip3 install tabulate
pip3 install cgecore
```

# Notes:
Online website:
https://cge.food.dtu.dk/services/IntFinder-1.0

IntFinder database expanded to detect integron classes 1, 2, and 3:
https://figshare.com/articles/dataset/intfinder_db/14096915
