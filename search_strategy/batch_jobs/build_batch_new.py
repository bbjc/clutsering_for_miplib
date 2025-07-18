import conf
import os
import pandas as pd

sh_template = """#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node=127
#SBATCH --exclusive
#SBATCH -c 1
#SBATCH -t 2-00:00:00
#SBATCH -p batch

cd
eval "$(micromamba shell hook --shell bash)"
micromamba activate clustering_for_mip

SCOOP_WRAPPER=$(pwd)/scoop-python.sh
cat << 'EOF' > "$SCOOP_WRAPPER"
#!/bin/bash -l
eval "$(micromamba shell hook --shell=bash)"
micromamba activate clustering_for_mip
python "$@"
EOF
chmod +x "$SCOOP_WRAPPER"

HOSTFILE=$(pwd)/hostfile
yes localhost | head -n 127 > "$HOSTFILE"

"""

if __name__ == "__main__":
    nb_gen = 20
    initial_pop = 100
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
                f'python -m scoop --hostfile "$HOSTFILE" -n 127 --python-interpreter="$SCOOP_WRAPPER" '
                f"{base_path}/genetic_programming_for_node_scoring.py "
                f"-problem MIPLIB "
                f"-nb_of_gen {nb_gen} "
                f"-initial_pop {initial_pop} "
                f"-fitness_size 5 "
                f"-time_limit {time_limit} "
                f"-seed {seed} "
                f"-nb_of_instances {nb_of_instances} "
                f"-cluster {cluster}\n"
                "micromamba deactivate\n"
            )

            script_name = f'miplib_seed_{seed}_nb_of_instances_{nb_of_instances}_time_limit_{time_limit}_cluster{cluster}.sh'
            script_path = os.path.join(saving_folder, script_name)

            with open(script_path, "w", newline="\n") as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)
