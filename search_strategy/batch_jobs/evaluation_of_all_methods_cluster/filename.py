import os

dossier = "search-strategy-generation-for-branch-and-bound-using-genetic-programming/batch_jobs/evaluation_of_all_methods_cluster/seed/"  
fichiers = [
    f for f in os.listdir(dossier)
    if os.path.isfile(os.path.join(dossier, f))
]


with open("liste_fichiers.txt", "w") as f_out:
    for f in fichiers:
        f_out.write(f + "\n")
