#!/bin/bash -l
#SBATCH -c 28
#SBATCH -t 2274
#SBATCH -p batch
#SBATCH --exclusive
cd
micromamba activate a_even_better_name_than_base
python -u node-selection-method-using-gp/evaluation_miplib_pb.py -function best_estimate_BFS -time_limit 120 -partition transfer