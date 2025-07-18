#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 10:38:45 2021

@author: abdel
"""


import os
import sys
import torch
import torch_geometric
from pathlib import Path
from model import GNNPolicy
from data_type import GraphDataset
from utils import process

if __name__ == "__main__":
    for problem in ['gisp','wpms','fcmcnf']:#,'wpms','fcmcnf'
        #problem = "gisp"
        lr = 0.005
        n_epoch = 2
        n_sample = 50
        patience = 10
        early_stopping = 20
        normalize = True
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        batch_train = 16
        batch_valid  = 256

        loss_fn = torch.nn.BCELoss()
        optimizer_fn = torch.optim.Adam
        #print(sys.argv)
        """for i in range(1, len(sys.argv), 2):
            if sys.argv[i] == '-problem':
                problem = str(sys.argv[i + 1])
            if sys.argv[i] == '-lr':
                lr = float(sys.argv[i + 1])
            if sys.argv[i] == '-n_epoch':
                n_epoch = int(sys.argv[i + 1])
            if sys.argv[i] == '-n_sample':
                n_sample = int(sys.argv[i + 1])
            if sys.argv[i] == '-patience':
                patience = int(sys.argv[i + 1])
            if sys.argv[i] == '-early_stopping':
                early_stopping = int(sys.argv[i + 1])
            if sys.argv[i] == '-normalize':
                normalize = bool(int(sys.argv[i + 1]))
            if sys.argv[i] == '-device':
                device = str(sys.argv[i + 1])
            if sys.argv[i] == '-batch_train':
                batch_train = int(sys.argv[i + 1])
            if sys.argv[i] == '-batch_valid':
                batch_valid = int(sys.argv[i + 1])"""



        train_losses = []
        valid_losses = []
        train_accs = []
        valid_accs = []

        dir = os.path.join(os.path.dirname(__file__)[:len(os.path.dirname(__file__))-34],
                                                                f"data\\{problem}\\train")
        #dir = f"C:\\Users\gwen.maudet\OneDrive - University of Luxembourg\Documents\programs\PycharmProjects\post doc lux\\GP2S\data\gips\\train"
        print(dir)
        train_files =[]
        for name in os.listdir(dir):
            if name[len(name)-3:]==".pt":
                train_files.append(os.path.join(os.path.dirname(__file__)[:len(os.path.dirname(__file__))-34],
                                                                f"data\\{problem}\\train\\") + str(name))

        """valid_files = [ str(path) for path in Path(os.path.join(os.path.dirname(__file__), 
                                                                f"../data/{problem}/valid")).glob("*.pt") ][:int(0.2*n_sample if n_sample != -1 else -1)]
        """

        """if problem == 'FCMCNF':
            train_files = train_files + valid_files[3000:]
            valid_files = valid_files[:3000]"""


        #print(train_files)
        train_data = GraphDataset(train_files)
        #print("aaaaaaa",train_data,len(train_data))
        #valid_data = GraphDataset(valid_files)


    # TO DO : learn something from the data
        train_loader = torch_geometric.loader.DataLoader(train_data,
                                                         batch_size=batch_train,
                                                         shuffle=True,
                                                         follow_batch=['constraint_features_s',
                                                                       'constraint_features_t',
                                                                       'variable_features_s',
                                                                       'variable_features_t'])

        """valid_loader = torch_geometric.loader.DataLoader(valid_data, 
                                                         batch_size=batch_valid, 
                                                         shuffle=False, 
                                                         follow_batch=['constraint_features_s',
                                                                       'constraint_features_t',
                                                                       'variable_features_s',
                                                                       'variable_features_t'])"""

        policy = GNNPolicy().to(device)
        optimizer = optimizer_fn(policy.parameters(), lr=lr) #ADAM is the best

        print("-------------------------")
        print(f"GNN for problem {problem}")
        print(f"Training on:          {len(train_data)} samples")
        #print(f"Validating on:        {len(valid_data)} samples")
        print(f"Batch Size Train:     {batch_train}")
        print(f"Batch Size Valid      {batch_valid}")
        print(f"Learning rate:        {lr} ")
        print(f"Number of epochs:     {n_epoch}")
        print(f"Normalize:            {normalize}")
        print(f"Device:               {device}")
        print(f"Loss fct:             {loss_fn}")
        print(f"Optimizer:            {optimizer_fn}")
        print(f"Model's Size:         {sum(p.numel() for p in policy.parameters())} parameters ")
        print("-------------------------")
        """torch.load("C:\\Users\gwen.maudet\OneDrive - University of Luxembourg\Documents\programs\PycharmProjects\post doc lux\\GP2S\data\gips\\train\\er_n=50_m=721_p=0.60_SET2_setparam=100.00_alpha=0.50.lp")
        print([[ind,tor] for ind,tor in enumerate(train_loader)])"""
        for epoch in range(n_epoch):
            print(f"Epoch {epoch + 1}")

            train_loss, train_acc = process(policy,
                                            train_loader,
                                            loss_fn,
                                            device,
                                            optimizer=optimizer,
                                            normalize=normalize)
            train_losses.append(train_loss)
            train_accs.append(train_acc)
            print(f"Train loss: {train_loss:0.3f}, accuracy {train_acc:0.3f}" )

            """valid_loss, valid_acc = process(policy, 
                                            valid_loader, 
                                            loss_fn, 
                                            device,
                                            optimizer=None,
                                            normalize=normalize)
            valid_losses.append(valid_loss)
            valid_accs.append(valid_acc)
            
            print(f"Valid loss: {valid_loss:0.3f}, accuracy {valid_acc:0.3f}" )"""

        torch.save(policy.state_dict(),f'policy_{problem}.pkl')





