import os
import json
import numpy as np
import conf
import math
import pandas as pd

def intersection_list(list1, list2):
   return list(set(list1) & set(list2))



def stats_comparison_GP_SCIP(table_size="reduced"):
    transformed_info = {}
    partition="test"

    functions = ["best_estimate_BFS","best_estimate_DFS",'SCIP']
    if table_size =='full':
        seeds =conf.seeds
    else:
        seeds = conf.reduced_seeds
    for seed in seeds:
        functions.append(f"GP_seed_{seed}")
    raw_perfs = {}
    transformed_info[partition] = {}
    feasibles_for_all = {}
    for function in functions:
        raw_perfs[function] = {}
        transformed_info[partition][function] = {}
        for time_limit in conf.time_limits:
            extracted_infos = conf.extract_GP_info_for_MIPLIB(time_limit, function, partition)
            if extracted_infos is not None:
                raw_perfs[function][time_limit] = extracted_infos
                transformed_info[partition][function][time_limit] = {"unfeasiblies":0,"mean_geo":0,"std_geo":0}
                list_of_feasibles=[]
                #csv_path = f"search-strategy-generation-for-branch-and-bound-using-genetic-programming/cluster_csv/hc_ward_method.csv"
                #df = pd.read_csv(csv_path)
                #cluster_1 = df[df["cluster"] == 4]["Instance"].tolist()
                #cluster_1_mps = [name.replace(".json", ".mps") if name.endswith(".json") else name + ".mps" for name in cluster_1]
                path = f"search-strategy-generation-for-branch-and-bound-using-genetic-programming/data/MIPLIB2017/miplib/"
                instances_set = os.listdir(path)
                #all_files = os.listdir(path)
                #instances_set = [f for f in all_files if f in cluster_1_mps]
                for instance in instances_set:
                    perf_of_the_instance = conf.find_perf_according_to_instance(extracted_infos, instance)
                    if perf_of_the_instance is None or perf_of_the_instance[1] ==1e+20:
                        transformed_info[partition][function][time_limit]["unfeasiblies"] +=1
                    else:
                        list_of_feasibles.append(instance)

                if time_limit not in feasibles_for_all.keys():
                    feasibles_for_all[time_limit] = list_of_feasibles
                else:
                    feasibles_for_all[time_limit] = intersection_list(feasibles_for_all[time_limit],
                                                                              list_of_feasibles)
                
            else:
                transformed_info[partition][function][time_limit] = {"unfeasiblies": 999, "mean_geo": 999, "std_geo": 999}
                print("problem extracted info none")

    for function in functions:
        for time_limit in conf.time_limits:
            extracted_infos = conf.extract_GP_info_for_MIPLIB(time_limit, function, partition)
            if extracted_infos is not None:
                perf_list = []
                for instance in feasibles_for_all[time_limit]:
                    perf_of_the_instance = conf.find_perf_according_to_instance(extracted_infos, instance)
                    perf_list.append(perf_of_the_instance[1])
                transformed_info[partition][function][time_limit]["std_geo"] = conf.geo_std(perf_list)
                transformed_info[partition][function][time_limit]["mean_geo"] = conf.shifted_geo_mean(perf_list)

    considered_times_for_table = conf.time_limits_for_paper 
    mini_inf = {}
    mini_gap = {}
    partition ="test"
    mini_inf[partition] = {}
    mini_gap[partition] = {}
    for time_limit in considered_times_for_table:
        mini_inf[partition][time_limit] = math.inf
        mini_gap[partition][time_limit] =  math.inf
        for function in functions:
            mini_inf[partition][time_limit] = min(mini_inf[partition][time_limit],transformed_info[partition][function][time_limit]["unfeasiblies"])
            mini_gap[partition][time_limit] = min(mini_gap[partition][time_limit],transformed_info[partition][function][time_limit]["mean_geo"])

    if table_size == "reduced":
        text = ""
        for time_limit in considered_times_for_table:
            text += f"&\multicolumn{{2}}{{c}}{{{time_limit} seconds}}"
        text += "\\\\"
        print(text)
        text = ""
        for time_limit in considered_times_for_table:
            text += f"&\\textsc{{Inf}} & \\textsc{{Gap}}"
        text += "\\\\"
        print(text)
        for function in functions:

            text = conf.proper_names[function]
            for time_limit in considered_times_for_table:
                c_inf, m_inf, y_inf, k_inf = conf.gradient_color(
                    transformed_info[partition][function][time_limit]["unfeasiblies"],
                    mini_inf[partition][time_limit],
                    mini_inf[partition][time_limit] * 1.2)
                c_gap, m_gap, y_gap, k_gap = conf.gradient_color(
                    transformed_info[partition][function][time_limit]["mean_geo"], mini_gap[partition][time_limit],
                    mini_gap[partition][time_limit] * 1.2)
                text += f' & \cellcolor[cmyk]{{{c_inf},{m_inf},{y_inf},{k_inf}}}$ {str(transformed_info[partition][function][time_limit]["unfeasiblies"])}$ & \cellcolor[cmyk]{{{c_gap},{m_gap},{y_gap},{k_gap}}}${str(transformed_info[partition][function][time_limit]["mean_geo"])}$$\pm$${str(transformed_info[partition][function][time_limit]["std_geo"])}$'
            text += '\\\\'
            print(text)

if __name__ == "__main__":
    stats_comparison_GP_SCIP("reduced")#full or reduced table
