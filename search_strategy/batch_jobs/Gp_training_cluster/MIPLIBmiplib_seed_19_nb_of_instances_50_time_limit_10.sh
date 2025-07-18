#!/bin/bash -l
#SBATCH -c 28
#SBATCH -t 2880
#SBATCH -p batch
#SBATCH --exclusive
cd
micromamba activate clustering_for_mip
python -u search-strategy-generation-for-branch-and-bound-using-genetic-programming/genetic_programming_for_node_scoring.py -problem MIPLIB -nb_of_gen 20 -initial_pop 20 -fitness_size 3 -time_limit 10 -seed 19 -nb_of_instances 50