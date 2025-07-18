#!/bin/bash -l
#SBATCH -c 28
#SBATCH -t 1895
#SBATCH -p batch
#SBATCH --exclusive
cd
micromamba activate clustering_for_mip
python -u search-strategy-generation-for-branch-and-bound-using-genetic-programming/MIPLIB_pbs/evaluation_miplib_pb.py -function best_estimate_DFS -time_limit 150 -partition transfer