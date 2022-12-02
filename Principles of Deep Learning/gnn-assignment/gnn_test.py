import dgl
from dgl.data import CoraGraphDataset
from dgl.dataloading import GraphDataLoader
import dgl.function as fn

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import networkx as nx
import math
transform = dgl.AddSelfLoop()  # by default, it will first remove self-loops to prevent duplication
dataset = CoraGraphDataset(transform=transform)
# Create dataset
dataset = CoraGraphDataset(transform=transform)
# only one graph exists with multiple nodes and edges
g = dataset[0]
device = torch.device('cpu')
g = g.int().to(device)
features = g.ndata['feat']
labels = g.ndata['label']
masks = g.ndata['train_mask'], g.ndata['val_mask'], g.ndata['test_mask']
n_classes = dataset.num_classes
# normalization
degs = g.in_degrees().float()
norm = torch.pow(degs, -0.5).to(device)
norm[torch.isinf(norm)] = 0
g.ndata['norm'] = norm.unsqueeze(1)


class CustomGNN(nn.Module):

    def __init__(self, in_feats, out_feats):
        '''
        ----------
        parameters
        ----------
        in_feats : int
            Input feature size; i.e, the number of dimensions of :math:`h_j^{(l)}`.
        out_feats : int
            Output feature size; i.e., the number of dimensions of :math:`h_i^{(l+1)}`.
        '''
        super(CustomGNN, self).__init__()
        self._theta = nn.Linear(in_feats, out_feats)
        self._phi = nn.Linear(in_feats, out_feats)

    def forward(self, graph, feat):
        '''
        ----------
        parameters
        ----------
        graph : DGLGraph
            The graph.
        feat : torch.Tensor or pair of torch.Tensor

        -------
        returns
        -------
        torch.Tensor
            The output feature
        '''
        with graph.local_scope():
            # TODO: Implement your GNN
            graph.srcdata['h'] = feat
            graph.dstdata['h'] = feat
            graph.ndata["first"] = feat
            func = lambda nodes: {'first': nodes.data["first"] - nodes.data["first"]}
            graph.apply_nodes(func)
            graph.ndata["first"] = self._theta(graph.ndata["first"])
            second = self._phi(feat)
            graph.srcdata["h"] = graph.ndata["first"] + second
            graph.update_all(fn.copy_src('h', 'm'), fn.max(msg = 'm', out = 'h'))
            return graph.dstdata['h']

class CustomClassifier(nn.Module):
    def __init__(self, in_dim, hidden_dim, n_classes):
        super(CustomClassifier, self).__init__()
        self.conv1 = CustomGNN(in_dim, hidden_dim)
        self.conv2 = CustomGNN(hidden_dim, hidden_dim)
        self.classify = nn.Linear(hidden_dim, n_classes)

    def forward(self, g, h):
        # TODO: Implement your classifier using the member modules in the class.
        h = F.relu(self.conv1(g, h))
        h = F.relu(self.conv2(g, h))
        g.ndata['h'] = h
        return self.classify(h)

# Create model
model = CustomClassifier(features.shape[1], 64, dataset.num_classes).to(device)
# define train/val samples, loss function and optimizer
train_mask = masks[0]
val_mask = masks[1]
loss_function = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

def evaluate(g, features, labels, mask, model):
    model.eval()
    with torch.no_grad():
        logits = model(g, features)
        logits = logits[mask]
        labels = labels[mask]
        _, indices = torch.max(logits, dim=1)
        correct = torch.sum(indices == labels)
        return correct.item() * 1.0 / len(labels)

loss = float('inf')
# training loop
# do not change the number of epochs, when submitting your final code
for epoch in range(100):
    model.train()
    acc = 0
    ##### TODO: #####
    # 1) get logits from the model
    logits = model(g, features)
    logits = logits[train_mask]
    tru_labels = labels[train_mask]
    # 2) calculate the loss using the loss function
    loss = loss_function(logits, tru_labels.to(device))
    # 3) backpropagate the loss
    optimizer.zero_grad()
    loss.backward()
    # 4) update the weights using the optimizer
    optimizer.step()
    epoch_loss = 0
    epoch_loss += loss.detach().item()
    #################
    acc = evaluate(g, features, labels, val_mask, model)
    print("Epoch {:05d} | Loss {:.4f} | Accuracy {:.4f} "
            . format(epoch, loss.item(), acc))