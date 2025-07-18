#!/bin/bash -l
#SBATCH -c 28
#SBATCH -t 540
#SBATCH -p batch
#SBATCH --exclusive
cd
micromamba activate clustering_for_mip
python -u search-strategy-generation-for-branch-and-bound-using-genetic-programming/MIPLIB_pbs/evaluation_miplib_pb.py -function seed_1 -time_limit 130 -partition test