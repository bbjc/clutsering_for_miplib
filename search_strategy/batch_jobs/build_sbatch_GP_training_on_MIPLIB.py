#import conf
#import os
#import json
#from pathlib import Path


#sh_template = """#!/bin/bash -l
#SBATCH -c 28
#SBATCH -t 2880
#SBATCH -p batch
#SBATCH --exclusive

#cd
#micromamba activate clustering_for_mip
 #   """
#if __name__ == "__main__":
  #  nb_gen = 20
  #  initial_pop = 20
  #  base_path = "/mnt/aiongpfs/users/bble/search-strategy-generation-for-branch-and-bound-using-genetic-programming"
  #  saving_folder = os.path.join(base_path, "batch_jobs", "Gp_training_cluster", "MIPLIB")
  #  sh_template = '#!/bin/bash -l\n#SBATCH -c 28\n#SBATCH -t 2880\n#SBATCH -p batch\n#SBATCH --exclusive\ncd\nmicromamba activate clustering_for_mip\n'

   # for seed in conf.seeds:
#            nb_of_instances = 50
 #           time_limit = 10
 #           to_print=sh_template + f'python -u search-strategy-generation-for-branch-and-bound-using-genetic-programming/genetic_programming_for_node_scoring.py -problem MIPLIB ##-nb_of_gen {nb_gen} -initial_pop {initial_pop} -fitness_size 3 -time_limit {time_limit} -seed {seed} -nb_of_instances {nb_of_instances}'
 #           name = f'miplib_seed_{seed}_nb_of_instances_{nb_of_instances}_time_limit_{time_limit}'
   #         file_path = saving_folder + name + f".sh"
#            with open(file_path
#                    ,
#                    "w",newline='\n') as outfile:
#                outfile.write(to_print)
#            os.chmod(file_path, 0o755)
            
            
import conf
import os
import pandas as pd

sh_template = """#!/bin/bash -l
#SBATCH -c 28
#SBATCH -t 2880
#SBATCH -p batch
#SBATCH --exclusive

cd
micromamba activate clustering_for_mip
"""

if __name__ == "__main__":
    nb_gen = 20
    initial_pop = 20
    nb_of_instances = 50
    time_limit = 10

    base_path = "/mnt/aiongpfs/users/bble/search-strategy-generation-for-branch-and-bound-using-genetic-programming"
    saving_folder = os.path.join(base_path, "batch_jobs", "Gp_training_cluster/hc_complete/")
    os.makedirs(saving_folder, exist_ok=True)

    # Charger le CSV
    csv_path = os.path.join(base_path, "cluster_csv/hc_complete_method.csv")
    df = pd.read_csv(csv_path)

    # Identifier les clusters distincts
    unique_clusters = df["cluster"].unique()

    for cluster in unique_clusters:
        for seed in conf.seeds:
            script_content = sh_template + (
                f"python -u search-strategy-generation-for-branch-and-bound-using-genetic-programming/genetic_programming_for_node_scoring.py "
                f"-problem MIPLIB "
                f"-nb_of_gen {nb_gen} "
                f"-initial_pop {initial_pop} "
                f"-fitness_size 3 "
                f"-time_limit {time_limit} "
                f"-seed {seed} "
                f"-nb_of_instances {nb_of_instances} "
                f"-cluster {cluster}"
            )

            script_name = f'miplib_seed_{seed}_nb_of_instances_{nb_of_instances}_time_limit_{time_limit}_cluster{cluster}.sh'
            script_path = os.path.join(saving_folder, script_name)

            with open(script_path, "w", newline="\n") as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)
