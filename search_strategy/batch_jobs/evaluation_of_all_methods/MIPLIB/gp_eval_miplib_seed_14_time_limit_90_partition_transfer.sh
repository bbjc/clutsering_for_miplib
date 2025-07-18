#!/bin/bash -l
#SBATCH -c 28
#SBATCH -t 1706
#SBATCH -p batch
#SBATCH --exclusive
cd
micromamba activate a_even_better_name_than_base
python -u node-selection-method-using-gp/evaluation_miplib_pb.py -function seed_14 -time_limit 90 -partition transfer