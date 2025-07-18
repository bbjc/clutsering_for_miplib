import os
import numpy as np
import scipy
import json
import math


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))




def shifted_geo_mean(iterable,shift=1,rounding=2):
    if rounding == 0:
        return round(np.exp(np.mean(np.log(np.array(iterable) + shift))) - shift)
    return round(np.exp(np.mean(np.log(np.array(iterable) + shift ))) - shift,rounding)
def geo_std(a,rounding=1):
    if rounding == 0:
        return round(np.exp(np.sqrt(np.mean((np.log(np.array(a) + 1) - np.log(shifted_geo_mean(a, 1))) ** 2))))
    return round(np.exp(np.sqrt(np.mean(  ( np.log(np.array(a)+1) - np.log(shifted_geo_mean(a,1)) )**2 ))),rounding)


def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

def gradient_color(value, min_val, max_val):### used for the plots
    if math.isnan(value):
        return (1,1,1)
    # Ensure the value is within the range [min_val, max_val]
    value = max(min_val, min(value, max_val))

    normalized_value = (value - min_val) / (max_val - min_val)

    c = round( 1 * (1 - normalized_value) ,2)
    m =round(normalized_value *1,2)
    y = 1
    k = round(0.25*normalized_value,2)

    return (c,m,y,k)








########## SPECIFIC TO ARTICIFIAL PROBLEMS

gp_funcs_artificial_problems = {'gisp': {'1.4': "sub(protectedDiv(getDepth, getEstimate), getDepth)",
                         "1.2": "sub(protectedDiv(getDepth, getEstimate), getDepth)"},
                "wpms": {'1.4': "protectedDiv(protectedDiv(protectedDiv(getDepth, getLowerbound), getNVars), getDepth)",
                         "1.2": "protectedDiv(getNConss, add(getEstimate, 10000000))"},
                "fcmcnf": {'1.4': "add(getDepth, protectedDiv(getEstimate, getDepth))",
                           "1.2": "protectedDiv(getEstimate, getDepth)"}}




########## SPECIFIC TO MIPLIB ##############
proper_names = {'best_estimate_BFS': "BE BFS","best_estimate_DFS": "BE DFS","best_LB_BFS": "LB BFS","gnn_bfs_nprimal=100000": "GNN full", "gnn_bfs_nprimal=2": "GNN 2 dives" , "GP_parsimony_parameter_1.2": "GP2S","GP_parsimony_parameter_1.4":"to remove","SCIP":"SCIP"}

for seed in range(1,21):
    proper_names[f"GP_seed_{seed}"] = f"GP2S {seed}"


def extract_GP_info_for_MIPLIB(time_limit, function, partition):
    folder = f"search-strategy-generation-for-branch-and-bound-using-genetic-programming/simulation_outcomes/MIPLIB/Evaluation/hc_complete/all"
    path =folder + f'/time_limit_{time_limit}_function_{function}_partition_{partition}.json'
    try:
        with open(path,'r') as openfile:
            perfs = json.load(openfile)
        return perfs
    except FileNotFoundError:
        print(f"Erreur : le fichier '{path}' est introuvable.")
    except json.JSONDecodeError:
        print(f"Erreur : le contenu du fichier '{path}' n'est pas un JSON valide.")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
 

def find_perf_according_to_instance(info,instance):
    for instance_of_folder,perf in zip(info["list_of_done"],info["performances"]):
        if instance_of_folder == instance:
            return perf
    return None




nbs_of_instances = [200,100,50]
time_limits = [10,50,150]
time_limits_for_paper = [10,50,150]#100,
#seeds = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
seeds = [1,2,3,4,5,6,7,8,9,10]
reduced_seeds = [1,2,3,4,5,6,7,8,9,10]

gp_funcs_MIPLIB_seeds1 = {'1':'add(getLowerbound, add(getLowerbound, getDepth))',
               '2':'add(getLowerbound, add(getLowerbound, getDepth))',
               '3':'mul(mul(getNVars, getLowerbound), add(add(add(getLowerbound, getDepth), getLowerbound), getLowerbound))',
               '4':'add(mul(add(getLowerbound, getDepth), getLowerbound), add(sub(mul(getLowerbound, getDualboundRoot), getLowerbound), getNVars))',
               '5':'add(add(getLowerbound, getDepth), getLowerbound)',
               '6':'add(add(getDepth, getLowerbound), getLowerbound)',
               '7':'add(add(getLowerbound, getDepth), getLowerbound)',
               '8':'add(add(getLowerbound, getDepth), getLowerbound)',
               '9':'mul(getLowerbound, add(add(add(sub(getLowerbound, getNVars), getDepth), getLowerbound), getLowerbound))',
               '10':'mul(add(getLowerbound, add(protectedDiv(getNConss, getEstimate), sub(getLowerbound, protectedDiv(getEstimate, getNConss)))), getLowerbound)'
               }
gp_funcs_MIPLIB_seeds2 = {'1':'add(getDepth, getEstimate)',
               '2':'add(getEstimate, sub(getDepth, 10000000))',
               '3':'add(sub(getLowerbound, sub(protectedDiv(mul(getEstimate, getNVars), sub(sub(sub(mul(getDepth, protectedDiv(getLowerbound, getLowerbound)), getNConss), mul(getLowerbound, add(getEstimate, protectedDiv(getLowerbound, getNVars)))), getDepth)), getLowerbound)), protectedDiv(getDepth, getDualboundRoot))',
               '4':'add(add(getEstimate, getNVars), getEstimate)',
               '5':'sub(mul(10000000, add(getNVars, getDepth)), sub(sub(getEstimate, getNVars), getLowerbound))',
               '6':'add(getEstimate, getEstimate)',
               '7':'add(getEstimate, getDepth)',
               '8':'add(getEstimate, getDepth)',
               '9':'add(getDepth, getEstimate)',
               '10':'add(getDepth, getEstimate)'
               }

gp_funcs_MIPLIB_seeds3 = {'1':'mul(protectedDiv(getNVars, protectedDiv(protectedDiv(sub(getNConss, add(mul(mul(add(getLowerbound, 10000000), getNConss), getDepth), mul(getLowerbound, getDepth))), mul(10000000, getLowerbound)), add(sub(getNVars, add(10000000, sub(getNConss, getNVars))), sub(getNVars, add(mul(10000000, getDepth), mul(sub(getNConss, getEstimate), getDepth)))))), 10000000)',
               '2':'sub(add(protectedDiv(getLowerbound, mul(getEstimate, getNVars)), getLowerbound), mul(getDepth, mul(getDepth, mul(getDualboundRoot, getEstimate))))',
               '3':'protectedDiv(sub(mul(10000000, getLowerbound), mul(sub(mul(getDualboundRoot, mul(10000000, getLowerbound)), sub(add(getEstimate, getEstimate), mul(mul(getEstimate, getLowerbound), getEstimate))), getDepth)), 10000000)',
               '4':'protectedDiv(getLowerbound, add(sub(add(add(sub(add(add(protectedDiv(getNVars, getEstimate), getLowerbound), getDepth), protectedDiv(protectedDiv(getEstimate, getLowerbound), getNVars)), getLowerbound), getDepth), protectedDiv(protectedDiv(getEstimate, getLowerbound), getNVars)), add(getEstimate, add(getDepth, getLowerbound))))',
               '5':'sub(add(mul(getEstimate, protectedDiv(getNVars, 10000000)), protectedDiv(getLowerbound, mul(getEstimate, protectedDiv(getNVars, getEstimate)))), protectedDiv(getDualboundRoot, add(mul(getEstimate, protectedDiv(protectedDiv(getLowerbound, getDepth), 10000000)), protectedDiv(getLowerbound, getDepth))))',
               '6':'add(mul(getLowerbound, sub(10000000, getEstimate)), protectedDiv(add(protectedDiv(getLowerbound, getEstimate), add(getNConss, mul(getLowerbound, sub(10000000, getLowerbound)))), getDepth))',
               '7':'sub(add(mul(mul(mul(getEstimate, getLowerbound), getLowerbound), sub(getDepth, mul(getDualboundRoot, mul(getDepth, mul(getLowerbound, getEstimate))))), add(getLowerbound, getDepth)), getEstimate)',
               '8':'protectedDiv(mul(getLowerbound, getLowerbound), add(getDepth, mul(protectedDiv(getNConss, getLowerbound), add(add(protectedDiv(getNConss, getLowerbound), getDepth), mul(getDepth, getEstimate)))))',
               '9':'add(sub(mul(mul(getNVars, getLowerbound), protectedDiv(getLowerbound, getDepth)), getEstimate), sub(mul(getNVars, getLowerbound), protectedDiv(getEstimate, add(getNVars, getDepth))))',
               '10':'protectedDiv(sub(mul(mul(getNVars, add(getLowerbound, getLowerbound)), getLowerbound), add(getEstimate, protectedDiv(sub(getNConss, add(getLowerbound, getNVars)), getDualboundRoot))), getDepth)'
               }
gp_funcs_MIPLIB_seeds4 = {'1':'protectedDiv(mul(10000000, sub(mul(getNConss, getDepth), getLowerbound)), getNVars)',
                '2':'protectedDiv(protectedDiv(getNVars, getLowerbound), getNVars)',
                '3':'sub(getDepth, sub(getEstimate, getNVars))',
                '4':'protectedDiv(getLowerbound, getDualboundRoot)',
                '5':'protectedDiv(getEstimate, sub(mul(getLowerbound, getDepth), getDepth))',
                '6':'protectedDiv(getLowerbound, getEstimate)',
                '7':'protectedDiv(getDepth, sub(mul(getNVars, getDualboundRoot), getLowerbound))',
                '8':'protectedDiv(getNVars, add(getLowerbound, getLowerbound))',
                '9':'protectedDiv(getDepth, add(getLowerbound, protectedDiv(getLowerbound, protectedDiv(getLowerbound, getLowerbound))))',
                '10':'protectedDiv(getDepth, getLowerbound)'
                }

gp_funcs_MIPLIB_seeds = {'1':'add(getLowerbound, add(getLowerbound, getDepth))',
                '2':'add(getLowerbound, add(getLowerbound, getDepth))',
                '3':'mul(mul(getNVars, getLowerbound), add(add(add(getLowerbound, getDepth), getLowerbound), getLowerbound))',
                '4':'add(mul(add(getLowerbound, getDepth), getLowerbound), add(sub(mul(getLowerbound, getDualboundRoot), getLowerbound), getNVars))',
                '5':'add(add(getLowerbound, getDepth), getLowerbound)',
                '6':'add(add(getDepth, getLowerbound), getLowerbound)',
                '7':'add(add(getLowerbound, getDepth), getLowerbound)',
                '8':'add(add(getLowerbound, getDepth), getLowerbound)',
                '9':'mul(getLowerbound, add(add(add(sub(getLowerbound, getNVars), getDepth), getLowerbound), getLowerbound))',
                '10':'mul(add(getLowerbound, add(protectedDiv(getNConss, getEstimate), sub(getLowerbound, protectedDiv(getEstimate, getNConss)))), getLowerbound)'
                }

instances_training = ['10teams.mps', '22433.mps', '23588.mps', 'acc-tight5.mps', 'app1-1.mps', 'app3.mps', 'assign1-5-8.mps', 'b-ball.mps', 'bab1.mps', 'beasleyC1.mps', 'berlin_5_8_0.mps', 'bg512142.mps', 'bienst1.mps', 'bienst2.mps', 'binkar10_1.mps', 'blend2.mps', 'bnatt400.mps', 'bppc4-08.mps', 'bppc8-09.mps', 'ci-s4.mps', 'cost266-UUE.mps', 'csched007.mps', 'csched008.mps', 'csched010.mps', 'danoint.mps', 'dcmulti.mps', 'drayage-25-27.mps', 'dsbmip.mps', 'fastxgemm-n2r6s0t2.mps', 'fastxgemm-n2r7s4t1.mps', 'g200x740.mps', 'gen-ip002.mps', 'gen-ip016.mps', 'gen-ip021.mps', 'gen-ip036.mps', 'gen-ip054.mps', 'ger50-17-ptp-pop-6t.mps', 'germany50-UUM.mps', 'glass4.mps', 'gmu-35-40.mps', 'gmu-35-50.mps', 'graphdraw-domain.mps', 'graphdraw-gemcutter.mps', 'graphdraw-mainerd.mps', 'gsvm2rl5.mps', 'gus-sch.mps', 'ic97_potential.mps', 'ic97_tension.mps', 'icir97_potential.mps', 'icir97_tension.mps', 'k16x240b.mps', 'khb05250.mps', 'l2p12.mps', 'lectsched-4-obj.mps', 'leo1.mps', 'leo2.mps', 'loopha13.mps', 'mad.mps', 'markshare1.mps', 'markshare2.mps', 'markshare_4_0.mps', 'markshare_5_0.mps', 'mas74.mps', 'mas76.mps', 'mcsched.mps', 'mik-250-20-75-3.mps', 'mik-250-20-75-5.mps', 'milo-v12-6-r2-40-1.mps', 'milo-v13-4-3d-3-0.mps', 'milo-v13-4-3d-4-0.mps', 'mkc.mps', 'n5-3.mps', 'n6-3.mps', 'n7-3.mps', 'neos-1067731.mps', 'neos-1423785.mps', 'neos-1442119.mps', 'neos-1582420.mps', 'neos-2624317-amur.mps', 'neos-2652786-brda.mps', 'neos-2657525-crna.mps', 'neos-3009394-lami.mps', 'neos-3024952-loue.mps', 'neos-3046601-motu.mps', 'neos-3046615-murg.mps', 'neos-3072252-nete.mps', 'neos-3083819-nubu.mps', 'neos-3118745-obra.mps', 'neos-3426085-ticino.mps', 'neos-3426132-dieze.mps', 'neos-3530903-gauja.mps', 'neos-3530905-gaula.mps', 'neos-3660371-kurow.mps', 'neos-3691541-lonja.mps', 'neos-3754480-nidda.mps', 'neos-4333596-skien.mps', 'neos-4393408-tinui.mps', 'neos-4650160-yukon.mps', 'neos-4738912-atrato.mps', 'neos-480878.mps', 'neos-4954672-berkel.mps', 'neos-5045105-creuse.mps', 'neos-5051588-culgoa.mps', 'neos-5107597-kakapo.mps', 'neos-5140963-mincio.mps', 'neos-5178119-nalagi.mps', 'neos-5182409-nasivi.mps', 'neos-5261882-treska.mps', 'neos-555424.mps', 'neos-555884.mps', 'neos-631517.mps', 'neos-686190.mps', 'neos-831188.mps', 'neos-911970.mps', 'neos-933562.mps', 'neos16.mps', 'neos5.mps', 'newdano.mps', 'nh97_potential.mps', 'nh97_tension.mps', 'ns1830653.mps', 'ns2071214.mps', 'nsa.mps', 'nu120-pr12.mps', 'opm2-z6-s1.mps', 'p500x2988.mps', 'pigeon-10.mps', 'pigeon-13.mps', 'pigeon-16.mps', 'pigeon-20.mps', 'pk1.mps', 'probportfolio.mps', 'prod1.mps', 'prod2.mps', 'qiu.mps', 'r50x360.mps', 'ran12x21.mps', 'ran13x13.mps', 'ran14x18-disj-8.mps', 'rentacar.mps', 'rocI-4-11.mps', 'rococoC10-001000.mps', 'roll3000.mps', 'sct2.mps', 'set3-09.mps', 'set3-10.mps', 'set3-16.mps', 'set3-20.mps', 'sp98ir.mps', 'supportcase20.mps', 'supportcase39.mps', 'swath.mps', 'swath2.mps', 'swath3.mps', 'tanglegram6.mps', 'timtab1.mps', 'timtab1CUTS.mps', 'tr12-30.mps', 'traininstance2.mps', 'traininstance6.mps', 'tw-myciel4.mps', 'uct-subprob.mps', 'umts.mps', 'usAbbrv-8-25_70.mps', 'v150d30-2hopcds.mps', 'wachplan.mps']

if __name__ == "__main__":
    ### modify the GP_function build from MIPLIB to the symbols used in the paper.
    for seed in gp_funcs_MIPLIB_seeds.keys():
        function = gp_funcs_MIPLIB_seeds[seed]
        function = function.replace("getDepth","d_i")
        function = function.replace("getEstimate", "BE_i")
        function = function.replace("getLowerbound", "z_i")
        function = function.replace("getDualboundRoot", "z_0")
        function = function.replace("getNConss", "m")
        function = function.replace("getNVars", "n")
        print(f"${seed}$ & ${function}$\\\\")
        
    
 
    #for ward method



# gp_funcs_MIPLIB_seeds1 = {'1':'protectedDiv(getDepth, getDualboundRoot)',
#                 '2':'sub(10000000, mul(sub(getNVars, getEstimate), protectedDiv(10000000, getDepth)))',
#                 '3':'mul(add(sub(getNConss, add(mul(mul(getDepth, getLowerbound), 10000000), getNVars)), mul(getNVars, mul(getDepth, add(getNVars, getNConss)))), mul(getEstimate, getNVars))',
#                 '4':'protectedDiv(getEstimate, sub(getNConss, add(getDualboundRoot, getEstimate)))',
#                 '5':'sub(add(getDepth, mul(getNVars, getDepth)), sub(sub(getNVars, sub(getDepth, sub(getNConss, sub(mul(getNVars, getDepth), getEstimate)))), getLowerbound))',
#                 '6':'mul(sub(add(getNConss, getEstimate), getDualboundRoot), getEstimate)',
#                 '7':'mul(getEstimate, sub(getLowerbound, protectedDiv(getEstimate, getNVars)))',
#                 '8':'protectedDiv(mul(add(10000000, getLowerbound), getEstimate), getLowerbound)',
#                 '9':'protectedDiv(10000000, add(10000000, getEstimate))',
#                 '10':'protectedDiv(protectedDiv(add(getLowerbound, getEstimate), getLowerbound), sub(getNVars, add(getNVars, getEstimate)))'
#                 }

# gp_funcs_MIPLIB_seeds2 = {'1':'mul(getNVars, getLowerbound)',
#                 '2':'add(getDepth, getLowerbound)',
#                 '3':'protectedDiv(getLowerbound, 10000000)',
#                 '4':'add(getDepth, getLowerbound)',
#                 '5':'add(getLowerbound, add(add(mul(getLowerbound, mul(getNVars, getLowerbound)), sub(protectedDiv(10000000, sub(getNVars, getDepth)), getNConss)), mul(add(getNConss, getNConss), getNConss)))',
#                 '6':'add(add(mul(mul(10000000, getLowerbound), getLowerbound), getEstimate), sub(mul(10000000, 10000000), getDualboundRoot))',
#                 '7':'sub(getLowerbound, sub(getDepth, getLowerbound))',
#                 '8':'protectedDiv(getDualboundRoot, add(getLowerbound, protectedDiv(sub(getDualboundRoot, mul(add(getLowerbound, getDepth), getDualboundRoot)), protectedDiv(getDepth, getDepth))))',
#                 '9':'add(add(getLowerbound, getDepth), getLowerbound)',
#                 '10':'add(getLowerbound, add(getDepth, getLowerbound))'
#                 }

# gp_funcs_MIPLIB_seeds3 = {'1':'add(getLowerbound, getLowerbound)',
#                 '2':'add(getDualboundRoot, getLowerbound)',
#                 '3':'sub(add(10000000, mul(getDualboundRoot, mul(getDualboundRoot, sub(mul(getLowerbound, getNConss), protectedDiv(getDepth, getDepth))))), mul(getLowerbound, add(10000000, getNConss)))',
#                 '4':'add(sub(getLowerbound, getNConss), getLowerbound)',
#                 '5':'add(getLowerbound, getLowerbound)',
#                 '6':'add(protectedDiv(getDepth, mul(sub(getLowerbound, add(getLowerbound, add(getNConss, mul(getLowerbound, getDepth)))), mul(add(protectedDiv(10000000, getDualboundRoot), getDepth), getNVars))), getLowerbound)',
#                 '7':'add(protectedDiv(getLowerbound, getEstimate), getDepth)',
#                 '8':'mul(getLowerbound, mul(protectedDiv(getNVars, protectedDiv(sub(10000000, getDepth), 10000000)), getNConss))',
#                 '9':'add(getLowerbound, protectedDiv(getLowerbound, getEstimate))',
#                 '10':'sub(getDepth, add(mul(getEstimate, getLowerbound), protectedDiv(getEstimate, 10000000)))'
#                 }
# gp_funcs_MIPLIB_seeds4 = {'1':'add(getLowerbound, add(getDepth, getLowerbound))',
#                '2':'add(getLowerbound, getDualboundRoot)',
#                '3':'add(add(mul(getDepth, getEstimate), sub(add(getEstimate, sub(getNVars, mul(getLowerbound, 10000000))), getDualboundRoot)), getLowerbound)',
#               '4':'add(getLowerbound, mul(10000000, getDualboundRoot))',
#                '5':'add(getLowerbound, getNConss)',
#                '6':'add(protectedDiv(10000000, getLowerbound), 10000000)',
#                '7':'add(getLowerbound, getLowerbound)',
#                '8':'add(getLowerbound, 10000000)',
#                '9':'add(10000000, getEstimate)',
#                '10':'add(getLowerbound, getLowerbound)'
#                }

# gp_funcs_MIPLIB_seeds5 = {'1':'protectedDiv(getLowerbound, mul(mul(getLowerbound, getNConss), mul(getLowerbound, getEstimate)))',
#                 '2':'sub(getLowerbound, mul(getLowerbound, add(10000000, getLowerbound)))',
#                 '3':'sub(add(10000000, mul(getDualboundRoot, getNVars)), mul(getLowerbound, add(getLowerbound, sub(10000000, getNVars))))',
#                 '4':'add(sub(getNVars, mul(getDualboundRoot, getLowerbound)), sub(10000000, getNVars))',
#                 '5':'protectedDiv(getNVars, sub(mul(protectedDiv(protectedDiv(getNConss, 10000000), getLowerbound), mul(getEstimate, 10000000)), getNVars))',
#                 '6':'protectedDiv(getDualboundRoot, mul(getDualboundRoot, getLowerbound))',
#                 '7':'protectedDiv(getLowerbound, getEstimate)',
#                 '8':'protectedDiv(sub(protectedDiv(getDepth, 10000000), add(getEstimate, add(getLowerbound, getLowerbound))), getLowerbound)',
#                 '9':'protectedDiv(getLowerbound, getEstimate)',
#                 '10':'add(getNVars, protectedDiv(10000000, add(getNConss, sub(getDepth, getLowerbound))))'
#                 }
# gp_funcs_MIPLIB_seeds6 = {'1':'mul(add(getDualboundRoot, add(getDepth, getEstimate)), getLowerbound)',
#                 '2':'sub(add(add(10000000, getDepth), getLowerbound), getDualboundRoot)',
#                 '3':'sub(getNVars, getEstimate)',
#                 '4':'mul(getEstimate, add(mul(getNVars, getLowerbound), sub(getDepth, getDualboundRoot)))',
#                 '5':'sub(protectedDiv(getDepth, protectedDiv(getDualboundRoot, add(getNVars, getEstimate))), getEstimate)',
#                 '6':'mul(getEstimate, add(10000000, getDualboundRoot))',
#                 '7':'sub(add(mul(getLowerbound, getEstimate), getNVars), getEstimate)',
#                 '8':'sub(protectedDiv(mul(10000000, getDualboundRoot), getEstimate), getEstimate)',
#                 '9':'mul(getEstimate, getLowerbound)',
#                 '10':'protectedDiv(getEstimate, add(protectedDiv(getDualboundRoot, protectedDiv(getLowerbound, getDepth)), protectedDiv(getDualboundRoot, 10000000)))'
#                 }
# gp_funcs_MIPLIB_seeds7 = {'1':'add(protectedDiv(protectedDiv(mul(getLowerbound, add(mul(getLowerbound, mul(add(10000000, getLowerbound), protectedDiv(getEstimate, getNVars))), protectedDiv(getNConss, mul(mul(getDepth, getDepth), getNVars)))), getLowerbound), getDepth), protectedDiv(getEstimate, 10000000))',
#                 '2':'mul(getLowerbound, mul(sub(protectedDiv(getEstimate, 10000000), getLowerbound), getLowerbound))',
#                 '3':'protectedDiv(add(getEstimate, getNVars), getLowerbound)',
#                 '4':'mul(getEstimate, add(mul(getNConss, getLowerbound), add(getLowerbound, getNVars)))',
#                 '5':'add(sub(add(10000000, getDualboundRoot), sub(getLowerbound, sub(getDepth, protectedDiv(mul(protectedDiv(mul(getNVars, sub(getDepth, getNConss)), getDepth), getDepth), protectedDiv(getLowerbound, getEstimate))))), getDualboundRoot)',
#                 '6':'protectedDiv(sub(mul(add(protectedDiv(getEstimate, getNVars), add(add(getNConss, 10000000), add(getNConss, protectedDiv(add(getLowerbound, protectedDiv(getEstimate, getNVars)), getEstimate)))), getLowerbound), getDepth), getDepth)',
#                 '7':'sub(add(mul(mul(getEstimate, getLowerbound), sub(getNConss, mul(getLowerbound, getDepth))), getDualboundRoot), getLowerbound)',
#                 '8':'add(mul(add(10000000, getDepth), getLowerbound), mul(sub(getDualboundRoot, mul(add(getLowerbound, add(getLowerbound, mul(add(getLowerbound, mul(add(getLowerbound, add(getLowerbound, mul(add(add(getDepth, getDepth), getDepth), getDualboundRoot))), getDualboundRoot)), getDualboundRoot))), getDualboundRoot)), mul(getEstimate, mul(add(getLowerbound, getDepth), getLowerbound))))',
#                 '9':'mul(mul(getLowerbound, getLowerbound), sub(add(getEstimate, getEstimate), sub(10000000, getNVars)))',
#                 '10':'protectedDiv(sub(mul(mul(sub(getEstimate, mul(getDepth, getNVars)), getEstimate), getDualboundRoot), protectedDiv(protectedDiv(getLowerbound, add(sub(mul(mul(getLowerbound, getEstimate), getDualboundRoot), protectedDiv(getLowerbound, add(getDepth, protectedDiv(getEstimate, 10000000)))), protectedDiv(getEstimate, 10000000))), getDepth)), protectedDiv(10000000, getLowerbound))'
#                 }
# gp_funcs_MIPLIB_seeds8 = {'1':'add(getNVars, add(getDepth, getNVars))',
#                 '2':'protectedDiv(getDepth, add(add(sub(getDepth, mul(getDepth, getEstimate)), getNVars), getNVars))',
#                 '3':'protectedDiv(mul(getEstimate, getDepth), add(add(add(getDepth, add(getEstimate, getEstimate)), getDepth), add(getEstimate, getEstimate)))',
#                 '4':'add(getDepth, protectedDiv(protectedDiv(getDepth, getDualboundRoot), protectedDiv(getNVars, getEstimate)))',
#                 '5':'protectedDiv(10000000, add(sub(sub(add(sub(sub(getEstimate, 10000000), 10000000), sub(getNConss, sub(getNConss, protectedDiv(mul(getNVars, sub(getDepth, protectedDiv(getNConss, sub(getDualboundRoot, 10000000)))), protectedDiv(getDualboundRoot, getEstimate))))), 10000000), getDualboundRoot), sub(getDualboundRoot, sub(add(getEstimate, getDualboundRoot), sub(getNConss, sub(sub(getEstimate, 10000000), protectedDiv(mul(getNVars, sub(getDepth, protectedDiv(getNConss, sub(getDualboundRoot, mul(getNConss, getNConss))))), getEstimate)))))))',
#                 '6':'add(protectedDiv(add(protectedDiv(getDepth, getNVars), add(add(getDualboundRoot, getDepth), getEstimate)), getNVars), getDepth)',
#                 '7':'add(getDepth, getDualboundRoot)',
#                 '8':'add(getDepth, mul(protectedDiv(getDepth, getDepth), protectedDiv(add(getDepth, getDualboundRoot), protectedDiv(mul(protectedDiv(getDepth, getNConss), getEstimate), mul(add(getDepth, getDualboundRoot), protectedDiv(add(getDepth, getDepth), mul(getLowerbound, 10000000)))))))',
#                 '9':'protectedDiv(protectedDiv(getEstimate, mul(getDepth, getNConss)), add(getDepth, getDepth))',
#                 '10':'protectedDiv(sub(sub(protectedDiv(getEstimate, getNConss), getDepth), 10000000), getDepth)'
#                 }   

                

# gp_funcs_MIPLIB_seeds = {'1':'add(getLowerbound, protectedDiv(getNVars, sub(getDepth, getNVars)))',
#                 '2':'add(add(getEstimate, getLowerbound), getNConss)',
#                 '3':'add(getLowerbound, protectedDiv(getDualboundRoot, getEstimate))',
#                 '4':'add(protectedDiv(getLowerbound, getDualboundRoot), mul(getNVars, getDepth))',
#                 '5':'protectedDiv(add(add(getEstimate, getNVars), getNVars), sub(getNConss, sub(getNVars, protectedDiv(getLowerbound, getNVars))))',
#                 '6':'mul(add(getEstimate, getLowerbound), add(getEstimate, getLowerbound))',
#                 '7':'add(add(mul(getLowerbound, getEstimate), getNVars), getEstimate)',
#                 '8':'sub(mul(getDualboundRoot, sub(add(10000000, sub(10000000, getLowerbound)), getEstimate)), mul(getDepth, getLowerbound))',
#                 '9':'protectedDiv(getDualboundRoot, protectedDiv(10000000, getEstimate))',
#                 '10':'protectedDiv(getLowerbound, protectedDiv(getNConss, getDepth))',
#                 '11': 'sub(protectedDiv(getDualboundRoot, getLowerbound), getNConss)',
#                 '12': 'protectedDiv(getLowerbound, mul(getDepth, add(add(getNVars, getEstimate), getDepth)))',
#                 '13': 'add(mul(sub(mul(getLowerbound, getLowerbound), getNVars), getNConss), protectedDiv(mul(getNVars, 10000000), mul(sub(mul(10000000, sub(getDepth, getDepth)), add(10000000, mul(getEstimate, sub(10000000, getNVars)))), add(getLowerbound, 10000000))))',
#                 '14': 'mul(mul(getLowerbound, protectedDiv(protectedDiv(getDepth, getLowerbound), getLowerbound)), sub(getEstimate, getNVars))',
#                 '15': 'mul(add(mul(add(add(getEstimate, add(getNVars, getEstimate)), getEstimate), getNVars), getEstimate), getEstimate)',
#                 '16': 'add(getLowerbound, getLowerbound)',
#                 '17': 'add(getEstimate, getLowerbound)',
#                 '18': 'add(sub(10000000, mul(getLowerbound, getDepth)), getEstimate)',
#                 '19': 'add(mul(getLowerbound, getDepth), protectedDiv(getEstimate, protectedDiv(protectedDiv(10000000, getDualboundRoot), protectedDiv(mul(getNVars, getDualboundRoot), 10000000))))',
#                 '20':'protectedDiv(protectedDiv(sub(getNVars, getNConss), 10000000), getEstimate)'
#                 }