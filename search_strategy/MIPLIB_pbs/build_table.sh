#!/bin/bash -l
#SBATCH -c 28
#SBATCH -t 2880
#SBATCH -p batch
#SBATCH --exclusive
cd
micromamba activate clustering_for_mip
python -u search-strategy-generation-for-branch-and-bound-using-genetic-programming/MIPLIB_pbs/build_table_MIPLIB_perfs.py
