import argparse
import os
import random
import pandas as pd # pour charger le csv et ensuite utiliser les instances avec leur classe 
import scip_solver
import conf

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="evaluate a GP_function candidate")
    parser.add_argument('comp_policy', type=str, help='comp_policy')
    parser.add_argument('problem', type=str, help='problem')
    parser.add_argument('training_folder', type=str, help='training_folder')
    parser.add_argument('node_select', type=str, help='node_select')
    parser.add_argument('time_limit', type=int, help='time_limit')
    parser.add_argument('seed', type=int, help='seed')
    parser.add_argument('nb_of_instances', type=int, help='nb_of_instances')
    parser.add_argument('cluster', type=int, help='cluster')
    args = parser.parse_args()
    if args.problem in ["gisp", "wpsm", "fcmcnf"]:
        lp_dir = os.path.join(os.path.dirname(__file__), f"data/{args.problem}/{args.training_folder}/")
        meannnodes, mean_val = scip_solver.perform_SCIP_instances_using_a_tuned_comp_policy(
            instances_folder=lp_dir,
            node_comp=args.comp_policy, node_select=args.node_select, parameter_settings=True)
        print(mean_val)
    else:
        random.seed(args.seed)

        df = pd.read_csv('search-strategy-generation-for-branch-and-bound-using-genetic-programming/cluster_csv/hc_complete_method.csv')
        cluster = args.cluster
        filename=df[df['cluster']==cluster]["Instance"].tolist()
        filenames = [os.path.splitext(f)[0] + '.mps' for f in filename]
        
        lp_dir = os.path.join(os.path.dirname(__file__), f"data/MIPLIB2017/miplib")
        training_indexes = random.sample(range(0, len(conf.instances_training)), args.nb_of_instances)
        # instances = [conf.instances_training[i] for i in training_indexes]
        instances = filenames
        instances_indexes = []
        index = 0
        for elt in os.listdir(lp_dir):
            if elt in instances:
                instances_indexes.append(index)
            index += 1
        meannnodes, mean_val = scip_solver.perform_SCIP_instances_using_a_tuned_comp_policy(
            instances_folder=lp_dir,
            node_comp=args.comp_policy, node_select=args.node_select, parameter_settings=True,
            time_limit=args.time_limit, instances_indexes=instances_indexes)
        print(mean_val)
        