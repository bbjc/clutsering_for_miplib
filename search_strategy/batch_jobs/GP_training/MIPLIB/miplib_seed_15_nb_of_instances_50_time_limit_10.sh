#!/bin/bash -l
#SBATCH -c 16
#SBATCH -t 2880
#SBATCH -p batch
#SBATCH --exclusive
cd
micromamba activate a_even_better_name_than_base
python -u node-selection-method-using-gp/genetic_programming_for_node_scoring.py -problem MIPLIB -nb_of_gen 18 -initial_pop 18 -fitness_size 3 -time_limit 10 -seed 15 -nb_of_instances 50