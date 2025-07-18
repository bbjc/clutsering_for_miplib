# Node Selection Method Using GP

## Installation

To set up your environment, run the following commands to install the required packages:
```bash
conda install deap matplotlib pyscipopt pytorch scipy
conda install -c conda-forge pytorch_geometric
```

## Folder Description

At the root of the project, you will find the files that are common to both parts of the experiment. The remaining directories are organized as follows:

- `data`: Contains everything related to the instances, including generation for artificial problems and extraction for MIPLIB 2017.
- `simulation_outcomes`: Stores the outputs of the algorithms, including GP functions and performance evaluations for both artificial problems and MIPLIB 2017.
- `batch_jobs`: Contains scripts that are executed on the HPC (High-Performance Computing) system.
- `artificial_pbs`: Contains files specific to the artificial problems studied.
- `learning_to_comparenodes`: Houses the GNN framework, with the `stats` directory which stores certain outputs from the method.
- `MIPLIB_pbs`: Contains files specific to MIPLIB 2017.


## Common Frameworks

This project is structured into two phases of simulations, both of which utilize common tools. The various Python files supporting these simulations are located in the root directory of the project.

The `conf.py` file consolidates all static data related to the problem, as well as foundational functions. For simplicity, functions derived through Genetic Programming (GP) methods are stored within this file.

### Solving Instances with a Tuned Node-Comparison Policy

The `scip_solver.py` file contains functions designed to solve instances using a specified search strategy, considering whether the resolution should be partial (with a time limit) or complete.

If the node-comparison policy is not SCIP, the function leverages `node_selection_policy.py` to generate a search strategy in SCIP format. In this case, the node-comparison policy can be defined as a function based on node and problem-specific information (i.e., the definition of the search strategy heuristic space). Since arguments are passed in a subprocess, the function can be defined as a string, which is then transformed into a scoring function.

### Genetic Programming Framework

The `genetic_programming_for_node_scoring.py` file implements the entire Genetic Programming (GP) algorithm, utilizing the DEAP package to simplify its implementation.

To train the GP algorithm, execute `genetic_programming_for_node_scoring.py` with the following parameters to specify various GP settings:

- `-problem`: Defines the problem type for training the GP (`gisp`, `wpms`, `fcmcnf` for artificial problems, or `miplib` for MIPLIB 2017).
- `-partition`: Default is `train`, indicating the folder containing training instances within `data/{problem}`.
- `-initial_pop`: Number of individuals in the population.
- `-nb_of_gen`: Number of generations.
- `-fitness_size`: Number of elements in the initial selection tournament based on fitness.
- `-parsimony_size`: Parameter related to the second tournament, which considers tree size.
- `-node_select`: Specifies the node selection method. The default is BFS, but it can be changed to DFS or a more advanced method.

Upon completion, the algorithm saves the results in the `simulation_outcomes/{problem}/GP_function` folder.

For the fitness evaluation phase, the genetic programming algorithm calls `subprocess_for_genetic.py` as a subprocess (to avoid core dump issues, which are discussed later in the document).

## Artificial Problems

The simulation phase focusing on artificial problems involves several key steps: generating instances for three types of problems, training machine learning methods (including our GP approach and the GNN baseline), and evaluating these ML methods alongside the SCIP built-in methods and additional heuristics. Files related to the GNN method are found in the `learning_to_comparenodes` directory, those for instance generation are in the `data` directory, and other specific files for this part of the project are in the `artificial_pbs` folder.

### Building Instances

To create the training, test, and transfer sets, run `data/build_{problem}_instances.py` (where `{problem}` is `gisp`, `wpms`, or `fcmcnf`) located in the `data` folder. Alternatively, you can use `subprocess_build_instances.py` to generate any set of instances in a single Python script.

In practice, only the training sets for the problems need to be generated.

### Training the GNN
For our experiments, we used the paper [Learning to Compare Nodes in Branch and Bound with Graph Neural Networks](https://arxiv.org/abs/2210.16934) as a baseline. We adapted their framework, available in the [learn2comparenodes GitHub repository](https://github.com/ds4dm/learn2comparenodes), which is included in our project under the `learning_to_comparenodes` folder.

Once the training set for a specific problem is prepared, run `node_selection/behaviour_gen.py` to generate a training set for the GNN, which compares pairs of nodes within a branch-and-bound process. These comparisons are stored in `.pt` format in the same folder as the instances they rely on. By default, the training set is generated for all three problem types.

Next, run `learning/train.py` to create and train a GNN model named `policy{problem}.pkl`, stored in the `learning` folder. This model is trained on the dataset generated by `behaviour_gen.py`. By default, training covers all three types of problems.

Finally, the script `subprocess_evaluation_gnn.py` is executed as a subprocess (triggered by `evaluation_gnn_gp_SCIPbaseline.py`) to evaluate the trained policies.

### Training the GP 

To train the GP function, run `genetic_programming_for_node_scoring.py` from the root directory with the appropriate settings.

The script `evaluation_convergence_of_GP_over_gens_artificial_pbs.py` generates the convergence plots for the GP, as shown in Figure 3 of Appendix B.

### Evaluation

After training the GNN and GP methods, they can be evaluated alongside the SCIP baseline and additional heuristics. Specifically, they are compared against best estimate BFS, DFS, and lowest lower bound BFS heuristics. Run `evaluation_gnn_gp_SCIPbaseline.py` to start the evaluation process. In this version, you must manually update the GP function (stored in `simulation_outcomes/{problem}/GP_function`) within `subprocess_evaluation_gp_SCIPbaseline.py`.

The function parameters include:
- `-problem`: Defines the problem type for evaluation (`gisp`, `wpms`, or `fcmcnf`).
- `-partition`: Specifies the partition to evaluate (`test` for instances similar to the training set or `transfer` for larger instances).

The function calls the following subprocesses to solve the instances in `problem/partition`:

- `subprocess_evaluation_gnn.py`: This script evaluates two methods—one where the GNN is used for two dives before switching to the best estimate, and another where the GNN is used throughout the solving process. In both cases, node selection is based on BFS.
- `subprocess_evaluation_gp_SCIPbaseline.py`: This script evaluates the GP method, the SCIP standalone method, and two heuristics—one using the best estimate and the other using the best lower bound, both within BFS.

### Table Construction

Based on the collected data, the script `build_tables_artificial_pb_perfs.py` constructs Table 2 in Section 5.1 of the main paper.

## MIPLIB 2017 Instances

### Extraction of MIPLIB Instances

MIPLIB 2017 instances are automatically downloaded from the official website [MIPLIB 2017](https://miplib.zib.de) using the script `data/MIPLIB2017/get_instances.py`. After downloading, the instances are unzipped using `data/MIPLIB2017/unzip_files.py`. The reduced set of instances is defined with the help of `data/MIPLIB2017/keep_easy_instances.py`, and the names of these instances are then stored in `conf.py`.
### Training the GP

To train the GP function, execute `genetic_programming_for_node_scoring.py` from the root directory with the appropriate settings. In the paper, we trained 20 different GP methods, each with a different seed to randomize the pool of training instances.

### Evaluation

The evaluation compares SCIP with handcrafted heuristics and the 20 seeded GP methods. It is conducted on both reduced and full MIPLIB 2017 instances, using different time limits per instance.

To perform the evaluation, run the file `evaluation_miplib_pb.py` with the following settings:

- `-function`: Define either SCIP, one of the handcrafted heuristics, or a GP-based heuristic specified as a string.
- `-time-limit`: Set the time limit for solving each instance.
- `-partition`: Choose either `test` for the reduced set or `transfer` for the full MIPLIB 2017 dataset.

This main function calls the Python file `subprocess_execution_MIPLIB.py` as a subprocess to solve each instance.

### Table Construction

The file `build_table_MIPLIB_perfs.py` generates Table 3 in Section 5.2 of the main paper and Table 6 in Appendix D.

## Technical Issues Encountered

### Instance Generation Settings

During our experiments, we identified a typo in the paper [Learning to Compare Nodes in Branch and Bound with Graph Neural Networks](https://arxiv.org/abs/2210.16934). The parameters for generating transfer instances were mistakenly swapped between the GISP and WPMS problem types. The corrected settings specify that the transfer parameters for GISP should be within the range [80,100], and for WPMS, they should be within [70,80]. These corrected parameters were used in our experiments.

### SCIP Baseline Definition

When defining evaluation baselines, we noticed a difference between our approach and that of the paper [Learning to Compare Nodes in Branch and Bound with Graph Neural Networks](https://arxiv.org/abs/2210.16934). Although both papers use the same name for the SCIP baseline, their version relies on a hardcoded variant, while we utilize the original SCIP version without any modifications to the standard search strategy.

### Core Dumps in SCIP

While solving some instances with tuned search strategies (either GP or GNN), we encountered situations where specific strategies caused SCIP to crash with a core dump. We reported this issue on their platform: [Error 0xC0000005 when changing the node selection method #819](https://github.com/scipopt/PySCIPOpt/issues/819).

To address this issue, we implemented subprocesses to prevent the entire algorithm from crashing. Our approach was as follows:
- For the GP algorithm, if a search strategy causes a core dump on a training set instance, it is discarded as a candidate and assigned a high score. This is managed by `subprocess_for_genetic.py`.
- For the artificial problem test and transfer phases, we generate new sets of instances and attempt to solve them using the GP-based search strategy, the GNN search strategy, and the SCIP baseline. If any method causes a core dump on an instance, the instance set is deleted and regenerated. The GNN method is evaluated by `subprocess_evaluation_gnn.py`, while the GP and SCIP baseline are evaluated by `subprocess_evaluation_pg_SCIPbaseline.py`.
- Similarly, for the MIPLIB instances, we solve each instance individually using the `subprocess_execution_MIPLIB.py` script. If an error occurs, we assign a score of 0 explored nodes and set the optimality gap to 1e+20.

### "Model Object No Longer Exists" During Resolution

In the MIPLIB experiments, we encountered situations where data from nodes or models became inaccessible during resolution. In such cases, SCIP automatically takes over to continue the resolution process without interruption. We observed that this issue tends to occur with very large instances. We are currently working with the SCIP support team to investigate this problem further.