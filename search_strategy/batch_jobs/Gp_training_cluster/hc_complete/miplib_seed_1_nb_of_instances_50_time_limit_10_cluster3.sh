#!/bin/bash -l
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

python -m scoop --hostfile "$HOSTFILE" -n 127 --python-interpreter="$SCOOP_WRAPPER" /mnt/aiongpfs/users/bble/search-strategy-generation-for-branch-and-bound-using-genetic-programming/genetic_programming_for_node_scoring.py -problem MIPLIB -nb_of_gen 20 -initial_pop 100 -fitness_size 5 -time_limit 10 -seed 1 -nb_of_instances 50 -cluster 3
micromamba deactivate
